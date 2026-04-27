from functions.text_cleansing.load_text import load_text
from functions.text_cleansing.to_lowercase import to_lowercase
from functions.text_cleansing.remove_punctuation import remove_punctuation
from functions.text_cleansing.tokenize import tokenize

def text_cleansing(file_path):
    """
    Full pipeline:
    file → lowercase → remove punctuation → tokenize
    """
    text = load_text(file_path)
    text = to_lowercase(text)
    text = remove_punctuation(text)
    words = tokenize(text)

    return words