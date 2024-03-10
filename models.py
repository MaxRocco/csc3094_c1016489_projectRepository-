from datetime import datetime
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
    lastLogin = db.Column(db.Date)

    allergic_to_celery = db.Column(db.Boolean, default=False)
    allergic_to_gluten = db.Column(db.Boolean, default=False)
    allergic_to_lupin = db.Column(db.Boolean, default=False)
    allergic_to_mustard = db.Column(db.Boolean, default=False)
    allergic_to_peanuts = db.Column(db.Boolean, default=False)
    allergic_to_sesame = db.Column(db.Boolean, default=False)
    allergic_to_soybeans = db.Column(db.Boolean, default=False)
    allergic_to_sulphur_dioxide = db.Column(db.Boolean, default=False)
    allergic_to_tree_nuts = db.Column(db.Boolean, default=False)

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

    mealID = db.Column(db.Integer, primary_key=True)
    mealName = db.Column(db.String(100), nullable=False)
    mealDescription = db.Column(db.Text, nullable=False)
    recipe = db.Column(db.Text, nullable=False)  # Store this as simple text? Probably.
    mealDifficulty = db.Column(db.Integer, default=1)  # Should look into difficulty later probably

    # Allergen fields for vegan food, directly within the Meal model, rather than through separate model + relationship
    # as I originally intended. Try how this works. I haven't included animal products, as it's assumed they aren't
    # present by default in any of the meals on my app, because it's for vegan cooking.

    # I have taken the allergens from https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses
    # (there are traditionally fourteen, though some the application assumes by default won't be present)
    # (SEE MY USER TERMS AND CONDITIONS FOR CLARIFICATION ON HOW ALLERGENS IN MEALS ARE HANDLED FOR USERS!!)
    # I will include more on these allergens in dissertation/documentation.

    # Also see https://www.anaphylaxis.org.uk/about-anaphylaxis/14-major-food-allergens/

    # I have removed Eggs, Fish, Milk, and Molluscs from this allergen list (not vegan). More on this in dissertation.

    contains_celery = db.Column(db.Boolean, default=False)
    contains_gluten = db.Column(db.Boolean, default=False)
    contains_lupin = db.Column(db.Boolean, default=False)
    contains_mustard = db.Column(db.Boolean, default=False)
    contains_peanuts = db.Column(db.Boolean, default=False)
    contains_sesame = db.Column(db.Boolean, default=False)
    contains_soybeans = db.Column(db.Boolean, default=False)
    contains_sulphur_dioxide = db.Column(db.Boolean, default=False)
    contains_tree_nuts = db.Column(db.Boolean, default=False)

    def __init__(self, mealName, mealDescription, recipe, mealDifficulty=1,
                 contains_celery=False, contains_gluten=False, contains_lupin=False, contains_mustard=False,
                 contains_peanuts=False, contains_sesame=False, contains_soybeans=False,
                 contains_sulphur_dioxide=False, contains_tree_nuts=False):
        self.mealName = mealName
        self.mealDescription = mealDescription
        self.recipe = recipe
        self.mealDifficulty = mealDifficulty
        self.contains_celery = contains_celery
        self.contains_gluten = contains_gluten
        self.contains_lupin = contains_lupin
        self.contains_mustard = contains_mustard
        self.contains_peanuts = contains_peanuts
        self.contains_sesame = contains_sesame
        self.contains_soybeans = contains_soybeans
        self.contains_sulphur_dioxide = contains_sulphur_dioxide
        self.contains_tree_nuts = contains_tree_nuts


# UserMeals model for tracking completed meals
class UserMeal(db.Model):
    __tablename__ = 'user_meals'
    # again, extend existing? See how this works first without.

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.mealID'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)  # I will later use this for user knowledge re-testing

    user = db.relationship('User',
                           back_populates='user_meals')  # back populate user meals to update info in there from here
    # (I think)
    meal = db.relationship('Meal')

    def __init__(self, user_id, meal_id, completed=False, completion_date=None):
        self.user_id = user_id
        self.meal_id = meal_id
        self.completed = completed
        if completed and completion_date is None:
            self.completion_date = datetime.utcnow()
        else:
            self.completion_date = completion_date


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
