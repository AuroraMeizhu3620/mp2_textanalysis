from load_text import load_text
from lowercase import to_lowercase
from remove_punctuation import remove_punctuation
from tokenize import tokenize

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