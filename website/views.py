from flask import Blueprint, render_template

from utils import get_words

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/words")
def words():
    words = get_words()
    return render_template("words.html", words=words)

