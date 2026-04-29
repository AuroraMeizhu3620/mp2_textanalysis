import nltk
from collections import Counter

nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

_STOP_WORDS = set(stopwords.words("english"))


def get_common_words(words, number_of_words=10):
    """Return the most common meaningful words using NLTK's English stopword list."""
    useful = [w for w in words if w not in _STOP_WORDS and len(w) > 2]
    return Counter(useful).most_common(number_of_words)
