import os
import sys

TEXT_CLEANING_FOLDER = os.path.join(os.path.dirname(__file__), "functions", "1.text_cleansing")
sys.path.insert(0, TEXT_CLEANING_FOLDER)

from text_cleansing import clean_text
from functions.framing_words.framing_analysis import analyze_framing
from functions.key_words.word_frequency import get_common_words


def analyze_article(title, source, text):
    """Run all analysis steps for one article."""
    words = clean_text(text)
    framing_results = analyze_framing(words)
    common_words = get_common_words(words)

    return {
        "title": title,
        "source": source,
        "text": text,
        "words": words,
        "common_words": common_words,
        "framing": framing_results,
    }


def compare_articles(article_a, article_b):
    """Create a small comparison summary for two analyzed articles."""
    difference = round(
        article_a["framing"]["negative_ratio"] - article_b["framing"]["negative_ratio"],
        2,
    )

    return {
        "article_a_ratio": article_a["framing"]["negative_ratio"],
        "article_b_ratio": article_b["framing"]["negative_ratio"],
        "difference": difference,
    }
