from datetime import datetime
from functools import wraps
import bcrypt
from flask import render_template
from flask_login import UserMixin, current_user
from app import app, db


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    requester_email = db.Column(db.String(100), nullable=False)
    requested_email = db.Column(db.String(100), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requested_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')

    requester = db.relationship('User', foreign_keys=[requester_id], back_populates='requested_friendships')
    requested = db.relationship('User', foreign_keys=[requested_id], back_populates='received_friendships')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='posts')


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
    quizzes_completed = db.Column(db.Integer, default=0)
    daily_experience = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    totalMeatCo2 = db.Column(db.Float, default=0)
    totalVeganCo2 = db.Column(db.Float, default=0)
    co2Reduction = db.Column(db.Float, default=0)
    co2ReductionPercent = db.Column(db.Float, default=0)

    allergic_to_celery = db.Column(db.Boolean, default=False)
    allergic_to_gluten = db.Column(db.Boolean, default=False)
    allergic_to_lupin = db.Column(db.Boolean, default=False)
    allergic_to_mustard = db.Column(db.Boolean, default=False)
    allergic_to_peanuts = db.Column(db.Boolean, default=False)
    allergic_to_sesame = db.Column(db.Boolean, default=False)
    allergic_to_soybeans = db.Column(db.Boolean, default=False)
    allergic_to_sulphur_dioxide = db.Column(db.Boolean, default=False)
    allergic_to_tree_nuts = db.Column(db.Boolean, default=False)

    user_meals = db.relationship('UserMeal', back_populates='user', lazy='dynamic')
    user_quizzes = db.relationship('UserQuiz', back_populates='user', lazy='dynamic')
    posts = db.relationship('Post', back_populates='user', lazy='dynamic')

    requested_friendships = db.relationship('Friendship', foreign_keys=[Friendship.requester_id],
                                            back_populates='requester', lazy='dynamic')
    received_friendships = db.relationship('Friendship', foreign_keys=[Friendship.requested_id],
                                           back_populates='requested', lazy='dynamic')

    def __init__(self, email, firstname, lastname, password, role, completed_onboarding):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.completed_onboarding = completed_onboarding


class Meal(db.Model):
    __tablename__ = 'meals'
    __table_args__ = {'extend_existing': True}

    mealID = db.Column(db.Integer, primary_key=True)
    mealName = db.Column(db.String(100), nullable=False)
    mealDescription = db.Column(db.Text, nullable=False)
    recipe = db.Column(db.Text, nullable=False)
    recipeInstructions = db.Column(db.Text, nullable=False)
    mealDifficulty = db.Column(db.Integer, default=1)
    imageUrl = db.Column(db.String(255), default=None)

    contains_celery = db.Column(db.Boolean, default=False)
    contains_gluten = db.Column(db.Boolean, default=False)
    contains_lupin = db.Column(db.Boolean, default=False)
    contains_mustard = db.Column(db.Boolean, default=False)
    contains_peanuts = db.Column(db.Boolean, default=False)
    contains_sesame = db.Column(db.Boolean, default=False)
    contains_soybeans = db.Column(db.Boolean, default=False)
    contains_sulphur_dioxide = db.Column(db.Boolean, default=False)
    contains_tree_nuts = db.Column(db.Boolean, default=False)

    veganCo2 = db.Column(db.Float, nullable=False)
    meatCo2 = db.Column(db.Float, nullable=False)

    def __init__(self, mealName, mealDescription, recipe, recipeInstructions, mealDifficulty=1, imageUrl=None,
                 contains_celery=False, contains_gluten=False, contains_lupin=False, contains_mustard=False,
                 contains_peanuts=False, contains_sesame=False, contains_soybeans=False,
                 contains_sulphur_dioxide=False, contains_tree_nuts=False, veganCo2=0.0, meatCo2=0.0):
        self.imageUrl = imageUrl
        self.mealName = mealName
        self.mealDescription = mealDescription
        self.recipe = recipe
        self.recipeInstructions = recipeInstructions
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
        self.veganCo2 = veganCo2
        self.meatCo2 = meatCo2


class UserMeal(db.Model):
    """Tracks the meals in which a user has completed within the meal progression tree"""
    __tablename__ = 'user_meals'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.mealID'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)

    user = db.relationship('User',
                           back_populates='user_meals')
    meal = db.relationship('Meal')

    def __init__(self, user_id, meal_id, completed=False, completion_date=None):
        self.user_id = user_id
        self.meal_id = meal_id
        self.completed = completed
        if completed and completion_date is None:
            self.completion_date = datetime.utcnow()
        else:
            self.completion_date = completion_date


class Quiz(db.Model):
    """Quiz model that is used to create new quizzes within the knowledge base page"""
    __tablename__ = 'quizzes'
    __table_args__ = {'extend_existing': True}

    quizID = db.Column(db.Integer, primary_key=True)
    quizName = db.Column(db.String(100), nullable=False)
    quizDescription = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=1)
    imageUrl = db.Column(db.String(255), default=None)

    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    user_quizzes = db.relationship('UserQuiz', back_populates='associated_quiz', lazy='dynamic')

    def __init__(self, quizName, quizDescription, order=1, imageUrl=None):
        self.quizName = quizName
        self.quizDescription = quizDescription
        self.order = order
        self.imageUrl = imageUrl


class Question(db.Model):
    """Defines questions that can be added to each quiz"""
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}

    questionID = db.Column(db.Integer, primary_key=True)
    quizID = db.Column(db.Integer, db.ForeignKey('quizzes.quizID'), nullable=False)
    questionText = db.Column(db.Text, nullable=False)
    correctAnswer = db.Column(db.String(100), nullable=False)
    otherOptions = db.Column(db.PickleType)  # easier than jsonify, which kept breaking

    def __init__(self, quizID, questionText, correctAnswer, otherOptions):
        self.quizID = quizID
        self.questionText = questionText
        self.correctAnswer = correctAnswer
        self.otherOptions = otherOptions


class UserQuiz(db.Model):
    """Tracks the quizzes in which a user has completed within the knowledge base or quizzes page"""
    __tablename__ = 'user_quizzes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quizID = db.Column(db.Integer, db.ForeignKey('quizzes.quizID'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completionDate = db.Column(db.DateTime)

    user = db.relationship('User',
                           back_populates='user_quizzes')
    associated_quiz = db.relationship('Quiz', back_populates='user_quizzes')

    def __init__(self, user_id, quizID, completed=False, completionDate=None):
        self.user_id = user_id
        self.quizID = quizID
        self.completed = completed
        if completed and completionDate is None:
            self.completionDate = datetime.utcnow()
        else:
            self.completionDate = completionDate


def init_db():
    """Initialises the database with a base user, that is useful when testing the application. Also includes some base
    meals and content for the meal progression tree, and initialises some quizzes within the knowledge base or quiz
    page. New quizzes, or meal recipes can be added here as desired, and get processed to the application automatically
    when the project is run. THIS FUNCTION WILL CLEAR EXISTING INFORMATION IN THE DATABASE AND RESET IT!

    It is important to note, that quiz and meal content have been generated by OpenAI’s ‘Chat Generative Pre-Trained
    Transformer, model 3.5’, and not by myself. This is for prototype demonstration purposes, and each meal recipe,
    quiz title, quiz questions and answers have been generated using artificial intelligence This is because I am not
    an expert in designing quiz questions or meal recipes, and the focus of this project is the computer science
    and software engineering aspects applied in creating this project, which have all been written by myself alone.

    Once again, quiz and meal recipe content, is purely mock up data.

    """
    from users.quizQuestions import easy_quiz, intermediate_quiz, advanced_quiz
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

        easyMeal = Meal(mealName="Simple Stir Fry", mealDescription="A simple and tasty stir fry meal, which is a "
                                                                    "core foundation in any home chefs repertoire of "
                                                                    "recipes!",
                        recipe="1 cup of cooked brown rice,"
                               "2 tablespoons olive oil,"
                               "1 sliced bell pepper,"
                               "1 cup of broccoli florets,"
                               "2 cloves of minced garlic,"
                               "2 tablespoons of soy sauce,"
                               "salt and pepper",
                        recipeInstructions="1. Heat the olive oil in a large pan over medium heat,"
                                           "2. Add the bell pepper, carrot, broccoli, and mushrooms. Sauté for about "
                                           "5-7 minutes or until vegetables are tender "
                                           "3. Add the minced garlic and sauté for another minute,"
                                           "4. In a small bowl, mix the soy sauce and maple syrup. Pour this mixture "
                                           "over the vegetables, "
                                           "5. Stir well to combine everything and cook for another 2 minutes,"
                                           "6. Serve the stir-fry over the cooked brown rice.",
                        mealDifficulty=1,
                        imageUrl="https://www.eatingbyelaine.com/wp-content/uploads/2023/10/EBE-Veggie-Stir-Fry-34.jpg",
                        veganCo2=1.5, meatCo2=2.3)

        intermediateMeal = Meal(mealName="Intermediate Vegetable Curry",
                                mealDescription="An intermediate vegetable curry, "
                                                "that is full of flavour and is "
                                                "guarenteed to enhance your cooking "
                                                "skills!",
                                recipe="2 tablespoons of coconut oil,"
                                       "1 chopped onion,"
                                       "1 chopped bell pepper,"
                                       "1 chopped carrot,"
                                       "1 cup of broccoli florets,"
                                       "1 cup of diced tomatoes (canned or fresh),"
                                       "1 tablespoon of curry powder,"
                                       "1 teaspoon of turmeric,"
                                       "1 can of coconut milk,"
                                       "Salt and pepper",
                                recipeInstructions="1. Use the cooked brown rice set aside from the "
                                                   "previous recipe or cook a fresh batch,"
                                                   "2. Heat coconut oil in a large pot over medium "
                                                   "heat, "
                                                   "3. Add the onion and sauté until translucent,"
                                                   "4. Add the bell pepper, carrot, and broccoli. "
                                                   "Cook for about 5 minutes, "
                                                   "5. Stir in the curry powder and turmeric, "
                                                   "cooking for another minute until fragrant, "
                                                   "6. Add the diced tomatoes and coconut milk. "
                                                   "Bring to a simmer, "
                                                   "7. Reduce heat and let it simmer for 15-20 "
                                                   "minutes, or until the vegetables are tender "
                                                   "and the flavors have melded together, "
                                                   "8. Season with salt and pepper,"
                                                   "9. Serve the curry over brown rice.",
                                mealDifficulty=2,
                                imageUrl="https://fullofplants.com/wp-content/uploads/2019/07/easy-spicy-vietnamese"
                                         "-curry-vegan-vegetarian-with-tofu-mushrooms-broccoli-taro-eggplant-24"
                                         "-1400x2100.jpg", veganCo2=1.2, meatCo2=2.6)

        advancedMeal = Meal(mealName="Advanced Stuffed Peppers",
                            mealDescription="An advanced and tasty recipe, that will provide a challenge to your "
                                            "vegan cooking skills, and enhance your overall ability nicely.",
                            recipe="4 large bell peppers, tops cut off and seeds removed,"
                                   "1 tablespoon olive oil,"
                                   "1 diced onion,"
                                   "2 cloves of minced garlic,"
                                   "1 diced carrot,"
                                   "1 cup of chopped mushrooms,"
                                   "1 cup of finely chopped broccoli florets,"
                                   "1 teaspoon of cumin,"
                                   "1 teaspoon of paprika,"
                                   "1 and a half cups of cooked brown rice,"
                                   "Salt and pepper",
                            recipeInstructions="1. Preheat the oven to 375°F (190°C),"
                                               "2. In a skillet, heat olive oil over medium heat. Add onion and "
                                               "garlic, and saute until onion is translucent, "
                                               "3. Add the carrot, mushrooms, and broccoli. Cook until vegetables are "
                                               "slightly tender, "
                                               "4. Stir in cumin, paprika, and then the cooked rice and mix well, "
                                               "5. Add the diced tomatoes and season with salt and pepper. Cook for a "
                                               "few more minutes until everything is heated through, "
                                               "6. Stuff the mixture into the hollowed-out bell peppers, "
                                               "7. Place the stuffed peppers in a baking dish and cover with foil, "
                                               "8. Bake for 30-35 minutes, or until the peppers are tender,"
                                               "9. Serve hot, possibly with a side of green salad",
                            mealDifficulty=3,
                            imageUrl="https://www.aheadofthyme.com/wp-content/uploads/2018/07/vegan-stuffed-peppers.jpg", veganCo2=2.3, meatCo2=3.4)

        easy_quiz()
        intermediate_quiz()
        advanced_quiz()

        db.session.add(user)
        db.session.add(baseUser)
        db.session.add(easyMeal)
        db.session.add(intermediateMeal)
        db.session.add(advancedMeal)

        db.session.commit()


def clear_db():
    """Deletes everything in the database when called, useful for testing. Do not include as part of a public version"""
    with app.app_context():
        db.drop_all()


# init_db() WILL RESET AND CLEAR THE DATABASE, COMMENT IT OUT IF YOU WANT TO PERSIST INFORMATION ACROSS RUN SESSIONS!
init_db()
