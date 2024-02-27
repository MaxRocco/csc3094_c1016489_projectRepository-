import logging
import bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user

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
            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, form.email.data, request.remote_addr)
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
                           lastname=current_user.lastname,
                           industry=current_user.industry,
                           region=current_user.region)


from models import User


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists', 'danger')
            return render_template('users/register.html', form=form)

        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data,
                        role='user')

        db.session.add(new_user)
        db.session.commit()

        logging.warning('SECURITY - Register [%s, %s]', form.email.data, request.remote_addr)

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('users.login'))

    # Flash validation errors to the user
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', 'danger')

    return render_template('users/register.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log Out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return redirect(url_for('index'))


