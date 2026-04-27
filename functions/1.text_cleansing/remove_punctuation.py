def remove_punctuation(text):
    """Remove punctuation manually without using string module."""
    
    cleaned_text = ""

    for char in text:
        # Keep letters, numbers, and spaces only
        if char.isalnum() or char.isspace():
            cleaned_text += char

    return cleaned_text