from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, NoneOf, ValidationError, Length, EqualTo, Regexp
import re


# Form for registering users
class RegisterForm(FlaskForm):

    def validate_password(self, password):

        p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])")

        if not p.match(password.data):
            raise ValidationError(
                "Password must contain at least one digit, one lowercase character, one uppercase character and one "
                "special character.")

    def validate_firstName(self, firstname):

        p = re.compile('[a-zA-Z0-9\s]+$')

        if not p.match(firstname.data):
            raise ValidationError(
                "Firstname must not include any of the following: * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >")

    def validate_lastName(self, lastname):

        p = re.compile('[a-zA-Z0-9\s]+$')

        if not p.match(lastname.data):
            raise ValidationError(
                "Lastname must not include any of the following: * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >")

    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), validate_firstName])
    lastname = StringField(validators=[DataRequired(), validate_lastName])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), validate_password])
    confirm_password = PasswordField(
        validators=[DataRequired(), EqualTo('password', message="The passwords entered must be equal.")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
