from . import db
from flask_login import UserMixin
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_german = db.Column(db.String(150), unique=True)
    definition_german = db.Column(db.String(150))
    definition_english = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    health = db.Column(db.Integer)
    score = db.Column(db.Integer)
    total_words = db.Column(db.Integer)