from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re


class RegisterForm(FlaskForm):
    """Registration form"""

    def validate_password(self, password):

        p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])")

        if not p.match(password.data):
            raise ValidationError(
                "Your password must contain at least one digit, one lowercase character, one uppercase character and "
                "one special character in order to be considered strong.")

    def validate_firstName(self, firstname):

        p = re.compile('[a-zA-Z0-9\s]+$')

        if not p.match(firstname.data):
            raise ValidationError(
                "Your firstname cannot include any of the following: * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >")

    def validate_lastName(self, lastname):

        p = re.compile('[a-zA-Z0-9\s]+$')

        if not p.match(lastname.data):
            raise ValidationError(
                "Your lastname cannot include any of the following: * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >")

    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), validate_firstName])
    lastname = StringField(validators=[DataRequired(), validate_lastName])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), validate_password])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo('password', message="Your passwords must be equal!")])
    accept_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
