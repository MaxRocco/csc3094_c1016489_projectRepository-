from functools import wraps
import bcrypt
from flask import render_template
from flask_login import UserMixin, current_user
from app import app, db


class User(db.Model, UserMixin):
    """Defines and initialises the user model, allows for user authentication"""

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    completed_onboarding = db.Column(db.Boolean, default=False)

    def __init__(self, email, firstname, lastname, password, role, completed_onboarding):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.completed_onboarding = completed_onboarding

def init_db():
    """Initialises the database with an example admin user"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(
            email='test@emailUser.com',
            firstname='Max',
            lastname='Ramage',
            password='userPassword!',
            role='user',
            completed_onboarding=True
        )
        baseUser = User(
            email='test@email.com',
            firstname='Jane',
            lastname='Doe',
            password='userPassword!',
            role='user',
            completed_onboarding=False
        )
        db.session.add(user)
        db.session.add(baseUser)
        db.session.commit()


def clear_db():
    """Deletes everything in the database"""
    with app.app_context():
        db.drop_all()


'''def required_roles(*roles):
    """Sets up role-based access control between users and admins"""
    import logging
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                logging.warning('SECURITY - Invalid Access Attempt')
                return render_template('errors/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper '''


'''The init_db() function is commented out, and will be called whenever models.py is ran if uncommented.
Be sure to call this function every time after running the test file, or when you first run the web application
in your own environment. '''

init_db()
