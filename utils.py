from website import models

from website.database import db


def get_words(*, skip: int = 0, limit: int = 100):
    return db.query(models.Word).offset(skip).limit(limit).all()
