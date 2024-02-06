from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.static.config')
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/content_management_db'

    db.init_app(app)

    with app.app_context():
        from . import views
        db.create_all()

    return app

migrate = Migrate(create_app, db)