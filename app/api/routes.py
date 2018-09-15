from app.api.models import Data
from apistar import http
from googletrans import Translator

extraction = Extraction()


def welcome(name=None):
    if name is None:
        return {"message": "Welcome to API Star!"}
    return {"message": f"Welcome to API Star, {name}!"}


def get_translation(word, language_destination="en", language_source="ru"):
    translator = Translator()
    word_translated = translator.translate(word, dest=language_destination, src=language_source).text

    return word_translated


def translate(data: Data):
    if data.word:
        word = data.word

    return get_translation(word)
