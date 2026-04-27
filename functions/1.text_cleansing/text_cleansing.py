from load_text import load_text


def clean_text(text):
    """
    Clean pasted text and return a list of words.

    Steps:
    1. make the text lowercase
    2. remove punctuation
    3. split the text into words
    """
    text = text.lower()

    cleaned_text = ""

    for char in text:
        if char.isalnum() or char.isspace():
            cleaned_text += char

    words = cleaned_text.split()

    return words


def text_cleansing(file_path):
    """
    Load text from a file, clean it, and return a list of words.
    This keeps the original file-based function working.
    """
    text = load_text(file_path)
    return clean_text(text)
