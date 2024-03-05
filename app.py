import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from users.views import users_blueprint

app.register_blueprint(users_blueprint)


@app.route('/')
def index():
    return render_template('main/index.html')


@app.errorhandler(400)
def badRequest_error(error):
    return render_template('errors/400.html')


@app.errorhandler(403)
def accessForbidden_error(error):
    return render_template('errors/403.html')


@app.errorhandler(404)
def pageNotFound_error(error):
    return render_template('errors/404.html')


@app.errorhandler(500)
def internalServer_error(error):
    return render_template('errors/500.html')


@app.errorhandler(503)
def serviceUnavailable_error(error):
    return render_template('errors/503.html')


if __name__ == '__main__':
    app.run()
