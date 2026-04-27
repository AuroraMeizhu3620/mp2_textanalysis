def load_text(file_path):
    """Load text from a file and return as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()