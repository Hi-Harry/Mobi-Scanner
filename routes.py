from flask import Blueprint, request, jsonify
from models import db, User, Contact, SpamReport
from auth import token_required
from utils import calculate_spam_likelihood
import jwt
from config import Config

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({"message": "Phone number already registered."}), 400
    user = User(name=data['name'], phone_number=data['phone_number'], email=data.get('email'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully."})

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(phone_number=data['phone_number']).first()
    if user and user.check_password(data['password']):
        token = jwt.encode({'id': user.id}, Config.SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({"message": "Invalid credentials"}), 401

@api.route('/contacts', methods=['POST'])
@token_required
def add_contact(current_user):
    data = request.get_json()
    contact = Contact(name=data['name'], phone_number=data['phone_number'])
    db.session.add(contact)
    db.session.commit()
    current_user.contacts.append(contact)
    db.session.commit()
    return jsonify({"message": "Contact added."})

@api.route('/spam', methods=['POST'])
@token_required
def report_spam(current_user):
    data = request.get_json()
    phone_number = data['phone_number']
    if not phone_number:
        return jsonify({"message": "Phone number required."}), 400
    report = SpamReport(phone_number=phone_number, reporter_id=current_user.id)
    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "Number marked as spam."})

@api.route('/search/phone', methods=['GET'])
@token_required
def search_by_phone(current_user):
    phone_number = request.args.get('phone_number')
    results = []
    registered_user = User.query.filter_by(phone_number=phone_number).first()
    if registered_user:
        spam_likelihood = calculate_spam_likelihood(phone_number, Contact, SpamReport)
        email = registered_user.email if current_user in registered_user.contacts else None
        results.append({
            "name": registered_user.name,
            "phone_number": registered_user.phone_number,
            "email": email,
            "spam_likelihood": spam_likelihood
        })
    else:
        contacts = Contact.query.filter_by(phone_number=phone_number).all()
        for c in contacts:
            spam_likelihood = calculate_spam_likelihood(c.phone_number, Contact, SpamReport)
            results.append({"name": c.name, "phone_number": c.phone_number, "spam_likelihood": spam_likelihood})
    return jsonify(results)

@api.route('/search/name', methods=['GET'])
@token_required
def search_by_name(current_user):
    name = request.args.get('name')
    starts = Contact.query.filter(Contact.name.like(f"{name}%")).all()
    contains = Contact.query.filter(Contact.name.like(f"%{name}%")).all()
    results = []
    seen = set()
    for c in starts + contains:
        if (c.name, c.phone_number) in seen:
            continue
        seen.add((c.name, c.phone_number))
        spam_likelihood = calculate_spam_likelihood(c.phone_number, Contact, SpamReport)
        results.append({"name": c.name, "phone_number": c.phone_number, "spam_likelihood": spam_likelihood})
    return jsonify(results)
