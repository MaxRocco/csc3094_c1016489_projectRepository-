import logging
from datetime import datetime, timedelta

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
                    daily_login_reward(user)
                return redirect(url_for('users.profile'))

    return render_template('users/login.html', form=form)


@users_blueprint.route('/profile')
@login_required
def profile():
    user_id = current_user.id

    return render_template('users/profile.html', name=current_user.firstname)


@users_blueprint.route('/account')
@login_required
def account():
    return render_template('users/account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname)


from models import User, Meal, UserMeal, Quiz, UserQuiz, Question, Friendship, Post


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

            if 'none' in allergens:
                current_user.allergic_to_celery = False
                current_user.allergic_to_gluten = False
                current_user.allergic_to_lupin = False
                current_user.allergic_to_mustard = False
                current_user.allergic_to_peanuts = False
                current_user.allergic_to_sesame = False
                current_user.allergic_to_soybeans = False
                current_user.allergic_to_sulphur_dioxide = False
                current_user.allergic_to_tree_nuts = False

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

    completed_meals_ids = {user_meal.meal_id for user_meal in current_user.user_meals.filter_by(completed=True).all()}

    nextMeal = None
    for meal in meals:
        if meal.mealID not in completed_meals_ids:
            nextMeal = meal
            break

    return render_template('users/mealTree.html', user=current_user, meals=meals,
                           completed_meals_ids=completed_meals_ids, next_meal=nextMeal)


@users_blueprint.route('/complete_meal/<int:meal_id>', methods=['POST'])
@login_required
def complete_meal(meal_id):
    reflection = request.form.get('reflection', '')
    makePublic = request.form.get('make_public') == 'true'

    if 500 < len(reflection) < 25:
        flash('Your reflection must be between 25 and 500 characters to mark this meal as complete!')
        return redirect(url_for('users.meal_detail', meal_id=meal_id))

    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()
    meal = Meal.query.get_or_404(meal_id)

    if not user_meal:
        new_user_meal = UserMeal(user_id=current_user.id, meal_id=meal_id, completed=True)
        db.session.add(new_user_meal)

    if user_meal and not user_meal.completed:
        user_meal.completed = True

    newPost = Post(
        user_id=current_user.id,
        email=current_user.email,
        title=f'Reflective account of {meal.mealName}',
        body=reflection,
        public=makePublic
    )
    db.session.add(newPost)

    exp_awarded = 25
    current_user.experiencePoints += exp_awarded
    current_user.meals_completed += 1

    db.session.commit()
    flash(f'Meal completed! + {exp_awarded} EXP. You can view your reflective account on the home page!')
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
        flash('No quiz has been found here')
        return redirect(url_for('users.knowledgeBase'))

    if user_quiz:
        user_quiz.completed = True
    else:
        new_user_quiz = UserQuiz(user_id=current_user.id, quizID=quizID, completed=True)
        db.session.add(new_user_quiz)

        questions = Question.query.filter_by(quizID=quizID).all()

        totalUserAnswers = []
        correctCount = 0
        totalQuestions = 0
        for question in questions:
            totalQuestions += 1
            userAnswer = request.form.get(f'question_{question.questionID}')
            isCorrect = userAnswer == question.correctAnswer
            totalUserAnswers.append((userAnswer, isCorrect))
            if userAnswer == question.correctAnswer:
                correctCount += 1

        correctQuestionExperience = correctCount * 2
        expAwarded = 2 + correctQuestionExperience  # 2 points for completion and additional 2 xp per correct answer
        current_user.experiencePoints += expAwarded

        current_user.quizzes_completed += 1

    db.session.commit()
    flash(f'Quiz completed! + {expAwarded} EXP. You scored {correctCount} out of a possible {totalQuestions} in that'
          f' quiz!')
    return redirect(url_for('users.reviewQuiz', quizID=quizID, user_answers=totalUserAnswers))


#    return redirect(url_for('users.knowledgeBase'))


@users_blueprint.route('/review_quiz/<int:quizID>')
@login_required
def reviewQuiz(quizID):
    userAnswers = request.args.getlist('totalUserAnswers')
    questions = Question.query.filter_by(quizID=quizID).all()

    questionAnswers = zip(questions, userAnswers)

    return render_template('users/reviewQuiz.html', questionAnswers=questionAnswers)


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
def shopping_list():
    return render_template('users/shoppingList.html', user=current_user)


def daily_login_reward(user):
    today = datetime.utcnow().date()
    loginRewardXP = 2

    if user.lastLogin != today:
        user.experiencePoints += loginRewardXP
        user.lastLogin = today

        flash(f"You have been awarded a daily login bonus of +{loginRewardXP} XP.")

        db.session.commit()


@users_blueprint.route('/search_users', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('query', '')
    if not query:
        flash('You must enter a user email before attempting to search!')
        return redirect(url_for('index'))

    searchResults = User.query.filter(
        User.id != current_user.id,
        (User.firstname.ilike(f'%{query}%') | User.lastname.ilike(f'%{query}%') | User.email.ilike(f'%{query}%'))
    ).all()

    return render_template('main/index.html', search_results=searchResults)


@users_blueprint.route('/send_friend_request/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
    targetUser = User.query.get(user_id)
    if not targetUser:
        flash('The user cannot be found')
        return redirect(url_for('index'))

    if targetUser.id == current_user.id:
        flash('You cannot send a friend request to yourself!')
        return redirect(url_for('index', user_id=user_id))

    existingRequest = Friendship.query.filter(
        ((Friendship.requester_id == current_user.id) & (Friendship.requested_id == user_id)) |
        ((Friendship.requester_id == user_id) & (Friendship.requested_id == current_user.id))
    ).first()

    if existingRequest:
        flash(f'You have already sent friends with {targetUser.email} or have sent a pending friend request to this '
              f'user!')
        return redirect(url_for('index', user_id=current_user.id))

    newRequest = Friendship(
        requester_id=current_user.id,
        requested_id=user_id,
        requester_email=current_user.email,
        requested_email=targetUser.email
    )
    db.session.add(newRequest)
    db.session.commit()
    flash(f'You have sent a friend request to {targetUser.email}!')
    return redirect(url_for('index', user_id=user_id))


@users_blueprint.route('/accept_friend_request/<int:request_id>', methods=['POST'])
@login_required
def accept_friend_request(request_id):
    friendship = Friendship.query.get(request_id)
    if friendship and friendship.requested_id == current_user.id:
        friendship.status = 'accepted'
        db.session.commit()
        flash('You have accepted this friend request!')
    else:
        flash('There is no pending friend requests here')
    return redirect(url_for('index'))


@users_blueprint.route('/decline_friend_request/<int:request_id>', methods=['POST'])
@login_required
def decline_friend_request(request_id):
    friendship = Friendship.query.get(request_id)
    if friendship and friendship.requested_id == current_user.id:
        friendship.status = 'declined'
        db.session.commit()
        flash('You have declined this user\'s friend request')
    else:
        flash('There is no pending friend request here')
    return redirect(url_for('index'))


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log Out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return redirect(url_for('index'))
