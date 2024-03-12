import logging
from datetime import datetime

import bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_user, current_user, login_required, logout_user
from flask_login import current_user

from app import db
from users.forms import RegisterForm, LoginForm

# from app import db
# from models import required_roles

# Blueprint configuration
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# Login user view
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash('No user found with that email', 'error')
        elif not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            logging.warning('SECURITY - Invalid Login Attempt [%s, %s]', form.email.data, request.remote_addr)
            flash('Incorrect password', 'error')
        else:
            login_user(user)
            logging.warning('SECURITY - Log in [%s, %s, %s]', user.id, form.email.data, request.remote_addr)

            if not user.completed_onboarding:
                return redirect(url_for('users.onboarding'))
            else:
                if user and user.is_authenticated:
                    dailyLoginReward(user)
                return redirect(url_for('users.profile'))

    return render_template('users/login.html', form=form)


# User profile view
@users_blueprint.route('/profile')
@login_required
def profile():
    user_id = current_user.id

    return render_template('users/profile.html', name=current_user.firstname)


# User account view
@users_blueprint.route('/account')
@login_required
def account():
    return render_template('users/account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname)


from models import User, Meal, UserMeal, Quiz, UserQuiz, Question


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if not form.accept_terms.data:
            flash('You must accept the terms and conditions to register.', 'danger')
            return render_template('users/register.html', form=form)

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists', 'danger')
            return render_template('users/register.html', form=form)

        new_user = User(
            email=form.email.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            password=form.password.data,  # I MUST HASH THIS BEFORE SUBMITTING, VERY IMPORTANT! (do later)
            role='user',
            completed_onboarding=False
        )

        db.session.add(new_user)
        db.session.commit()

        logging.warning('SECURITY - Register [%s, %s]', form.email.data, request.remote_addr)

        login_user(new_user)

        flash('Registration successful')
        return redirect(url_for('users.onboarding'))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', 'danger')

    return render_template('users/register.html', form=form)


@users_blueprint.route('/termsAndConditions')
def terms_and_conditions():
    return render_template('users/termsAndConditions.html')


@users_blueprint.route('/updateAllergies', methods=['GET', 'POST'])
@login_required
def updateAllergies():
    current_user.allergic_to_celery = False
    current_user.allergic_to_gluten = False
    current_user.allergic_to_lupin = False
    current_user.allergic_to_mustard = False
    current_user.allergic_to_peanuts = False
    current_user.allergic_to_sesame = False
    current_user.allergic_to_soybeans = False
    current_user.allergic_to_sulphur_dioxide = False
    current_user.allergic_to_tree_nuts = False

    if request.method == 'POST':
        if 'allergen' in request.form:
            allergens = request.form.getlist('allergen')

            for allergen in allergens:
                if allergen == 'celery':
                    current_user.allergic_to_celery = True
                elif allergen == 'gluten':
                    current_user.allergic_to_gluten = True
                elif allergen == 'lupin':
                    current_user.allergic_to_lupin = True
                elif allergen == 'mustard':
                    current_user.allergic_to_mustard = True
                elif allergen == 'peanuts':
                    current_user.allergic_to_peanuts = True
                elif allergen == 'sesame':
                    current_user.allergic_to_sesame = True
                elif allergen == 'soybeans':
                    current_user.allergic_to_soybeans = True
                elif allergen == 'sulphur_dioxide':
                    current_user.allergic_to_sulphur_dioxide = True
                elif allergen == 'tree_nuts':
                    current_user.allergic_to_tree_nuts = True

            flash("Allergy information updated!")
            db.session.commit()
            return redirect(url_for('users.profile'))

    return render_template('users/updateAllergies.html', user=current_user)


@users_blueprint.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if not current_user or current_user.completed_onboarding:
        return redirect(url_for('users.profile'))

    if 'allergen' in request.form:
        allergens = request.form.getlist('allergen')

        for allergen in allergens:
            if allergen == 'celery':
                current_user.allergic_to_celery = True
            elif allergen == 'gluten':
                current_user.allergic_to_gluten = True
            elif allergen == 'lupin':
                current_user.allergic_to_lupin = True
            elif allergen == 'mustard':
                current_user.allergic_to_mustard = True
            elif allergen == 'peanuts':
                current_user.allergic_to_peanuts = True
            elif allergen == 'sesame':
                current_user.allergic_to_sesame = True
            elif allergen == 'soybeans':
                current_user.allergic_to_soybeans = True
            elif allergen == 'sulphur_dioxide':
                current_user.allergic_to_sulphur_dioxide = True
            elif allergen == 'tree_nuts':
                current_user.allergic_to_tree_nuts = True

    if request.method == 'POST':
        if 'completed_onboarding' in request.form:
            current_user.completed_onboarding = True
            db.session.commit()
            flash('Onboarding completed successfully!')
            return redirect(url_for('users.profile'))

    return render_template('users/onboarding.html', user=current_user)


@users_blueprint.route('/mealTree')
@login_required
def mealTree():
    meals = Meal.query.order_by(Meal.mealDifficulty).all()

    completed_meals_ids = [user_meal.meal_id for user_meal in current_user.user_meals.filter_by(completed=True).all()]

    return render_template('users/mealTree.html', user=current_user, meals=meals,
                           completed_meals_ids=completed_meals_ids)


@users_blueprint.route('/complete_meal/<int:meal_id>', methods=['POST'])
@login_required
def complete_meal(meal_id):
    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()

    meal = Meal.query.get(meal_id)
    if not meal:
        flash('Meal not found.')
        return redirect(url_for('users.mealTree'))

    if user_meal:
        user_meal.completed = True
    else:
        new_user_meal = UserMeal(user_id=current_user.id, meal_id=meal_id, completed=True)
        db.session.add(new_user_meal)

        exp_awarded = 25  # * meal.mealDifficulty with base 10 perhaps for additional satisfaction?
        current_user.experiencePoints += exp_awarded

        current_user.meals_completed += 1

    db.session.commit()
    flash(f'Meal completed! + {exp_awarded} EXP.')
    return redirect(url_for('users.mealTree'))


@users_blueprint.route('/meal_detail/<int:meal_id>')
@login_required
def meal_detail(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()

    completed = user_meal and user_meal.completed

    return render_template('users/mealDetails.html', meal=meal, completed=completed)


@users_blueprint.route('/knowledgeBase')
@login_required
def knowledgeBase():
    quizzes = Quiz.query.order_by(Quiz.order).all()

    completed_quizzes_IDs = [user_quiz.quizID for user_quiz in
                             current_user.user_quizzes.filter_by(completed=True).all()]

    return render_template('users/knowledgeBase.html', user=current_user, quizzes=quizzes,
                           completed_quiz_IDs=completed_quizzes_IDs)


@users_blueprint.route('/complete_quiz/<int:quizID>', methods=['POST'])
@login_required
def complete_quiz(quizID):
    user_quiz = UserQuiz.query.filter_by(user_id=current_user.id, quizID=quizID).first()

    quiz = Quiz.query.get(quizID)
    if not quiz:
        flash('Quiz not found.')
        return redirect(url_for('users.knowledgeBase'))

    if user_quiz:
        user_quiz.completed = True
    else:
        new_user_quiz = UserQuiz(user_id=current_user.id, quizID=quizID, completed=True)
        db.session.add(new_user_quiz)

        exp_awarded = 10  # * for additional satisfaction look at this later like with meals
        current_user.experiencePoints += exp_awarded

        current_user.quizzes_completed += 1

    db.session.commit()
    flash(f'Quiz completed! + {exp_awarded} EXP.')
    return redirect(url_for('users.knowledgeBase'))


@users_blueprint.route('/quiz_detail/<int:quizID>')
@login_required
def quiz_detail(quizID):
    quiz = Quiz.query.get_or_404(quizID)
    questions = Question.query.filter_by(quizID=quizID).all()
    user_quiz = UserQuiz.query.filter_by(user_id=current_user.id, quizID=quizID).first()

    completed = user_quiz and user_quiz.completed

    return render_template('users/quizDetails.html', questions=questions, quiz=quiz, completed=completed)


@users_blueprint.route('/shoppingList')
@login_required
def shoppingList():
    return render_template('users/shoppingList.html', user=current_user)


def dailyLoginReward(user):
    today = datetime.utcnow().date()
    loginRewardXP = 2

    if user.lastLogin != today:
        user.experiencePoints += loginRewardXP
        user.lastLogin = today

        flash(f"You have been awarded a daily login bonus of +{loginRewardXP} XP.")

        db.session.commit()


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log Out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return redirect(url_for('index'))
