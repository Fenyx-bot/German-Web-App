import requests
from bs4 import BeautifulSoup
import json

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from website import models
from website.database import db


class GermanWord:
    def __init__(self, word, article, gender, c) -> None:
        """
        word: str
        article: str
        gender: str
        c: str (alterantive to class)
        """
        self.word = word
        self.article = article
        self.gender = gender
        self.c = c


class Word:
    def __init__(self, word, word_english, definition, definition_english) -> None:
        self.word = word
        self.word_english = word_english
        self.definition = definition
        self.definition_english = definition_english

    @staticmethod
    def from_html(html) -> "Word | None":
        try:
            word = html.find("span", class_="wlv-item__word").text.strip()
            word_english = html.find("span", class_="wlv-item__english").text.strip()
            sample = html.find("div", class_="wlv-item__samples-box")
            definition = sample.find("span", class_="wlv-item__word").text.strip()
            definition_english = sample.find(
                "span", class_="wlv-item__english"
            ).text.strip()

            return Word(word, word_english, definition, definition_english)

        except Exception as e:
            print("Failed to parse the word: ", e)

        return None

    @staticmethod
    def from_dict(json):
        return Word(
            json["word"],
            json["word_english"],
            json["definition"],
            json["definition_english"],
        )

    def to_dict(self):
        return {
            "word": self.word,
            "word_english": self.word_english,
            "definition": self.definition,
            "definition_english": self.definition_english,
        }

    def __str__(self) -> str:
        return f"{self.word} ({self.word_english}) - {self.definition} ({self.definition_english})"


url = "https://www.germanpod101.com/german-word-lists/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}


def scrape_words(page_num: int) -> list[Word]:
    response = requests.get(f"{url}?page={page_num}", headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        words = []
        # Further processing

        containers = soup.find_all("div", class_="wlv-item js-wlv-item")

        for container in containers:
            if container is None:
                continue

            word = Word.from_html(container)

            if word is None:
                continue

            print("Word: ", word)

            words.append(word)

        return words

    else:
        print("Failed to retrieve the page.")

    return []


def fill_database(db: Session, words: list[Word]) -> None:
    for word in words:
        try:
            word_model = models.Word(
                word_german=word.word,
                word_english=word.word_english,
                definition_german=word.definition,
                definition_english=word.definition_english,
            )

            print("Adding word: ", word)
            db.add(word_model)

        except IntegrityError:
            print("Word already exists: ", word)

        except Exception as e:
            print("Failed to add the word: ", word, e)

    db.commit()


def scrape(*, use_file=True):
    """
    use_file: bool

    If True, it won't scrape and will use the words.json file if it exists.
    """
    file_name = "words.json"

    if use_file:
        try:
            with open(file_name, "r") as f:
                json_data = json.load(f)
                words = [Word.from_dict(word) for word in json_data]

                print("Got words: ", len(words))

                fill_database(db, words)

                return
        except FileNotFoundError:
            print("File not found.")

    pages = 5
    words = []
    for i in range(1, pages + 1):
        words.append(scrape_words(i))

    words = [word for sublist in words for word in sublist]

    json_data = [word.to_dict() for word in words]

    print("Got words: ", len(words))

    with open(file_name, "w") as f:
        json.dump(json_data, f, indent=4)

    fill_database(db, words)
