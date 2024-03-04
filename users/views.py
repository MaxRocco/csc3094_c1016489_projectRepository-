import logging
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

            # Redirect to onboarding page if the user hasn't completed onboarding
            if not user.completed_onboarding:
                return redirect(url_for('users.onboarding'))
            else:
                # Redirect to profile page if onboarding is completed
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


from models import User, Meal, UserMeal


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

        flash('Registration successful', 'success')
        return redirect(url_for('users.onboarding'))

    # Flash validation errors to the user
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', 'danger')

    return render_template('users/register.html', form=form)



#         return redirect(url_for('onboarding'))
#     return render_template('register.html')

@users_blueprint.route('/onboarding', methods=['GET', 'POST'])
@login_required  # Ensures that only logged-in users can access this route
def onboarding():
    # Since we're using Flask-Login, we can directly use current_user
    if not current_user or current_user.completed_onboarding:
        return redirect(url_for('users.profile'))

    if request.method == 'POST':
        if 'completed_onboarding' in request.form:
            current_user.completed_onboarding = True
            db.session.commit()
            flash('Onboarding completed successfully!', 'success')
            return redirect(url_for('users.profile'))
        # Here you can handle other actions like going to the next step

    # Render the current step of the onboarding process
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
    # Check if the meal is already marked as completed
    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()

    if user_meal:
        user_meal.completed = True
    else:
        new_user_meal = UserMeal(user_id=current_user.id, meal_id=meal_id, completed=True)
        db.session.add(new_user_meal)

    db.session.commit()
    return redirect(url_for('users.mealTree'))


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log Out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return redirect(url_for('index'))
