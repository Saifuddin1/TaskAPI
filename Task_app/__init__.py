
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

 
db = SQLAlchemy()
DATABASE = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "@hello123"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
    db.init_app(app)
    from .show import show
    from .validation import validation

    
    app.register_blueprint(show, url_prefix = "/")
    app.register_blueprint(validation, url_prefix = "/")

    from . models import User,Task
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "validation.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) 


    return app

def create_database(app):
    if not path.exists("Blog_app/" + DATABASE):
        with app.app_context():
            db.create_all()
        print("Created database")