import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)

_analyzer = None


def _get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def analyze_sentiment(text):
    """
    Run VADER sentiment analysis on the full article text.

    VADER gives a compound score from -1 (most negative) to +1 (most positive),
    plus proportions of positive, negative, and neutral language.
    """
    scores = _get_analyzer().polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    # compound_pct maps -1..+1 to 0..100 for the CSS position marker
    compound_pct = round((compound + 1) / 2 * 100, 1)

    return {
        "compound": round(compound, 3),
        "compound_pct": compound_pct,
        "positive": round(scores["pos"] * 100, 1),
        "negative": round(scores["neg"] * 100, 1),
        "neutral": round(scores["neu"] * 100, 1),
        "label": label,
    }
