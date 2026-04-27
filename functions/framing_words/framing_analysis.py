from collections import Counter


# This list is intentionally simple and visible.
# You can edit it when you want the project to use a different definition.
NEGATIVE_FRAMING_WORDS = {
    "accused", "aggression", "alleged", "attack", "attacks", "ban",
    "banned", "charged", "charges", "clash", "clashed", "condemned",
    "conflict", "crime", "crimes", "criminal", "crisis", "criticism",
    "death", "defence", "destroy", "extremist", "facing", "fear",
    "forced", "humanity", "invasion", "killed", "killing", "opposition",
    "protest", "punish", "rights", "risk", "threat", "violence", "war",
    "warrants", "whitewashing",
}


def find_framing_words(words):
    """Return a list of words that match the framing word list."""
    matches = []

    for word in words:
        if word in NEGATIVE_FRAMING_WORDS:
            matches.append(word)

    return matches


def analyze_framing(words):
    """Calculate framing word statistics for one article."""
    framing_words = find_framing_words(words)
    framing_counts = Counter(framing_words)

    total_words = len(words)
    total_framing_words = len(framing_words)

    if total_words == 0:
        negative_ratio = 0
    else:
        negative_ratio = round((total_framing_words / total_words) * 100, 2)

    return {
        "total_words": total_words,
        "total_framing_words": total_framing_words,
        "negative_ratio": negative_ratio,
        "common_framing_words": framing_counts.most_common(10),
    }
