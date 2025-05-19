import random
from faker import Faker
from models import db, User, Contact
from app import app

fake = Faker()

with app.app_context():
    for _ in range(20):
        u = User(name=fake.name(), phone_number=fake.phone_number(), email=fake.email())
        u.set_password("test123")
        db.session.add(u)
    db.session.commit()

    users = User.query.all()
    for user in users:
        for _ in range(5):
            c = Contact(name=fake.name(), phone_number=fake.phone_number())
            db.session.add(c)
            user.contacts.append(c)
    db.session.commit()

    print("Sample data added.")

