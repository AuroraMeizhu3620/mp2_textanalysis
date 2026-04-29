from collections import Counter

# Transparent, editable list of negatively-framed political words.
# Edit this set to widen or narrow the definition for your presentation.
NEGATIVE_FRAMING_WORDS = {
    "accused", "aggression", "alleged", "attack", "attacks", "ban",
    "banned", "charged", "charges", "clash", "clashed", "condemned",
    "conflict", "crime", "crimes", "criminal", "crisis", "criticism",
    "death", "deaths", "destroy", "destroyed", "extremist", "extremists",
    "fear", "forced", "invasion", "killed", "killing", "occupation",
    "oppression", "protest", "punish", "punishment", "repression",
    "rights", "risk", "threat", "threats", "violence", "violent",
    "war", "warfare", "whitewashing",
}


def find_framing_words(words):
    """Return tokens from the article that appear in the framing word list."""
    return [w for w in words if w in NEGATIVE_FRAMING_WORDS]


def analyze_framing(words):
    """Calculate framing word statistics for one article's token list."""
    framing_words = find_framing_words(words)
    framing_counts = Counter(framing_words)
    total_words = len(words)
    total_framing = len(framing_words)
    negative_ratio = round((total_framing / total_words) * 100, 2) if total_words else 0

    return {
        "total_words": total_words,
        "total_framing_words": total_framing,
        "negative_ratio": negative_ratio,
        "common_framing_words": framing_counts.most_common(10),
    }
