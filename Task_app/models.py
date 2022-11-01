from . import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String(120),unique = True)
    username = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(120),unique = True)
    contact = db.Column(db.String(15),unique = True)
    tasks = db.relationship('Task',backref ='user',passive_deletes = True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empact = db.Column(db.Integer)
    ease = db.Column(db.Integer)
    confidence = db.Column(db.Integer)
    average = db.Column(db.Float)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)


