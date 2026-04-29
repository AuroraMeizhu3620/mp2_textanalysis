import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def clean_text(text):
    """
    Tokenize and clean article text using NLTK.

    Uses word_tokenize for accurate handling of contractions and punctuation,
    then keeps only alphabetic tokens lowercased.
    """
    tokens = word_tokenize(text.lower())
    return [token for token in tokens if token.isalpha()]
