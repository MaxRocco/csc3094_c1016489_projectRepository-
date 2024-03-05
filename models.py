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
    experiencePoints = db.Column(db.Integer, default=0)
    meals_completed = db.Column(db.Integer, default=0)

    # Experiment with back_populates='user' relationship and dynamic loading of information
    user_meals = db.relationship('UserMeal', back_populates='user', lazy='dynamic')

    def __init__(self, email, firstname, lastname, password, role, completed_onboarding):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.completed_onboarding = completed_onboarding


class Meal(db.Model):
    __tablename__ = 'meals'
    # extend existing?

    mealID = db.Column(db.Integer, primary_key=True)
    mealName = db.Column(db.String(100), nullable=False)
    mealDescription = db.Column(db.Text, nullable=False)
    recipe = db.Column(db.Text, nullable=False)  # Store this as simple text? Probably.
    mealDifficulty = db.Column(db.Integer, default=1)  # To order meals by difficulty, for progression tree.

    def __init__(self, mealName, mealDescription, recipe, mealDifficulty=1):
        self.mealName = mealName
        self.mealDescription = mealDescription
        self.recipe = recipe
        self.mealDifficulty = mealDifficulty


# UserMeals model for tracking completed meals
class UserMeal(db.Model):
    __tablename__ = 'user_meals'
    # again, extend existing? See how this works first without.

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.mealID'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)  # This may come in useful later for retesting users on info.

    user = db.relationship('User',
                           back_populates='user_meals')  # back populate user meals to update info in there from here (I think)
    meal = db.relationship('Meal')

    # I want to put completion date, not sure if to do it in the init or not. Figure out later.
    def __init__(self, user_id, meal_id, completed):
        self.user_id = user_id
        self.meal_id = meal_id
        self.completed = completed


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

        new_meal1 = Meal(mealName="Test Meal 1", mealDescription="Peppery fooBar meal.", recipe="Peppers, Rice",
                         mealDifficulty=1)
        new_meal2 = Meal(mealName="Test Meal 2", mealDescription="Peppery fooBar meal2.", recipe="Peppers, Rice",
                         mealDifficulty=2)

        db.session.add(user)
        db.session.add(baseUser)
        db.session.add(new_meal1)
        db.session.add(new_meal2)
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
