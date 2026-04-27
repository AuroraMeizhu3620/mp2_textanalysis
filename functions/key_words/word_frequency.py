from collections import Counter


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "their", "this", "to", "was", "were", "will", "with", "would",
}


def count_words(words):
    """Count how many times each word appears."""
    return Counter(words)


def get_common_words(words, number_of_words=10):
    """Return the most common meaningful words."""
    useful_words = []

    for word in words:
        if word not in STOP_WORDS and len(word) > 2:
            useful_words.append(word)

    word_counts = count_words(useful_words)
    return word_counts.most_common(number_of_words)
