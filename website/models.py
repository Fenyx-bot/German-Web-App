from flask_login import UserMixin
from sqlalchemy.sql.functions import current_timestamp
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    username = Column(String(150), unique=True)
    date_created = Column(DateTime, default=current_timestamp())


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    word_german = Column(String(150))
    word_english = Column(String(150))
    definition_german = Column(String(150))
    definition_english = Column(String(150))
    date_created = Column(DateTime, default=current_timestamp())


class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    health = Column(Integer)
    score = Column(Integer)
    total_words = Column(Integer)

