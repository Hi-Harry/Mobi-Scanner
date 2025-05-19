from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

contact_association = db.Table('contact_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contacts = db.relationship('Contact', secondary=contact_association, backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    spam_reports = db.Column(db.Integer, default=0)

class SpamReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
