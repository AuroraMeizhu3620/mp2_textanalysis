import os
import sys

# word_tokenize lives in a folder with a dot in its name, so we add it to the path manually
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "functions", "1.text_cleansing"))

from text_cleansing import clean_text
from functions.framing_words.framing_analysis import analyze_framing
from functions.key_words.word_frequency import get_common_words
from functions.sentiment.sentiment_analysis import analyze_sentiment
from functions.summary.openai_analysis import analyze_with_openai


def analyze_article(title, source, text):
    """Run the full analysis pipeline for one article."""
    words = clean_text(text)
    framing_results = analyze_framing(words)
    common_words = get_common_words(words)
    sentiment = analyze_sentiment(text)      # VADER runs on the original text, not tokens
    ai_analysis = analyze_with_openai(text)  # contextual framing analysis via OpenAI

    return {
        "title": title,
        "source": source,
        "text": text,
        "words": words,
        "common_words": common_words,
        "framing": framing_results,
        "sentiment": sentiment,
        "ai_analysis": ai_analysis,
    }


def compare_articles(article_a, article_b):
    """Build a side-by-side comparison of framing ratio and VADER sentiment."""
    diff_ratio = round(
        article_a["framing"]["negative_ratio"] - article_b["framing"]["negative_ratio"], 2
    )
    diff_sentiment = round(
        article_a["sentiment"]["compound"] - article_b["sentiment"]["compound"], 3
    )

    if diff_sentiment > 0:
        more_negative = "B"
    elif diff_sentiment < 0:
        more_negative = "A"
    else:
        more_negative = None

    return {
        "article_a_ratio": article_a["framing"]["negative_ratio"],
        "article_b_ratio": article_b["framing"]["negative_ratio"],
        "difference": diff_ratio,
        "article_a_compound": article_a["sentiment"]["compound"],
        "article_b_compound": article_b["sentiment"]["compound"],
        "sentiment_difference": abs(diff_sentiment),
        "more_negative": more_negative,
    }
