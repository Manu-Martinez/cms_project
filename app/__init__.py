from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os 
from dotenv import load_dotenv
from . import loginManager

db = SQLAlchemy()
migrate = Migrate()
loginManager = LoginManager()

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)
    loginManager.init_app(app)

    with app.app_context():
        from .static import views   # noqa: F401
        db.create_all()  # Create the database tables

    return app

@loginManager.user_loader
def load_user(user_id):
	from .static.models import User  # Import here to avoid circular import
	return User.query.get(int(user_id))
