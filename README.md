# mp2_textanalysis

A Python and Flask text analysis app that examines how news articles frame events through language.

This project follows the original proposal goal: compare how different news platforms describe conflicts, protests, and political events through word choice. The app is inspired by the idea of "Permission to Narrate" and looks for patterns in tone, bias, and negatively connotated language.

## What The App Does

The proposal listed this workflow:

User pastes article text -> app cleans the text -> app counts key words -> app detects framing words -> app creates a chart -> user compares Article A vs. Article B

The current app supports that workflow with:

- A Flask web page where users can paste Article A and Article B.
- Text cleaning using the existing `functions/1.text_cleansing` folder.
- Common word counts in `functions/key_words`.
- Negative framing word detection in `functions/framing_words`.
- Basic statistics: total words, framing word count, and negative framing ratio.
- Simple visual bar charts made with HTML and CSS.
- A search page that uses the free GDELT API to find articles from selected sources.

## Important Note About Article Search

The app uses GDELT because it is free and does not require an API key. GDELT is good for searching article links by topic and source, but it does not always provide full article text. The app tries to fetch article paragraphs from the article URL, but some news websites block automatic fetching.

If fetching fails, open the article link, copy the article text, and paste it into the analysis page.

## Project Structure

```text
app.py
analysis_pipeline.py
requirements.txt
templates/
static/
data/
functions/
    1.text_cleansing/
    key_words/
    framing_words/
    article_sources/
```

## How To Run

Install Flask:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

## Files To Edit As The Project Grows

- `functions/framing_words/framing_analysis.py`: edit the framing word list.
- `functions/key_words/word_frequency.py`: edit stop words or number of common words.
- `functions/article_sources/gdelt_source.py`: add or remove searchable news sources.
- `templates/index.html`: change the analysis page layout.
- `templates/search.html`: change the search page layout.

## Fairness Reminder

The proposal asks how to define "negative framing" words fairly. The current list is a starter list, not a final political judgment. For a stronger presentation, explain that the list is transparent, editable, and should be tested across multiple articles and sources.
