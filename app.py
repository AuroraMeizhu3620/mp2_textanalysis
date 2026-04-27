from flask import Flask, render_template, request

from analysis_pipeline import analyze_article, compare_articles
from functions.article_sources.gdelt_source import (
    SOURCE_DOMAINS,
    fetch_article_text,
    search_articles,
)


app = Flask(__name__)


def build_article_from_form(letter):
    """Read one article box from the form and analyze it."""
    title = request.form.get("title_" + letter, "").strip()
    source = request.form.get("source_" + letter, "").strip()
    text = request.form.get("text_" + letter, "").strip()

    if title == "":
        title = "Article " + letter.upper()

    if source == "":
        source = "Pasted text"

    if text == "":
        return None

    return analyze_article(title, source, text)


@app.route("/", methods=["GET", "POST"])
def index():
    article_a = None
    article_b = None
    comparison = None
    error = ""

    if request.method == "POST":
        article_a = build_article_from_form("a")
        article_b = build_article_from_form("b")

        if article_a is None and article_b is None:
            error = "Paste text into at least one article box before analyzing."

        if article_a is not None and article_b is not None:
            comparison = compare_articles(article_a, article_b)

    return render_template(
        "index.html",
        article_a=article_a,
        article_b=article_b,
        comparison=comparison,
        error=error,
        sources=SOURCE_DOMAINS,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    articles = []
    error = ""
    selected_source = "The Guardian"
    search_text = ""
    fetched_text = ""
    fetched_url = ""

    if request.method == "POST":
        action = request.form.get("action", "search")
        selected_source = request.form.get("source", selected_source)
        search_text = request.form.get("search_text", "").strip()

        if action == "search":
            if search_text == "":
                error = "Type a search topic first."
            else:
                try:
                    articles = search_articles(search_text, selected_source)
                except Exception as problem:
                    error = "The article search did not work: " + str(problem)

        if action == "fetch":
            fetched_url = request.form.get("article_url", "").strip()

            if fetched_url == "":
                error = "Choose an article URL first."
            else:
                try:
                    fetched_text = fetch_article_text(fetched_url)

                    if fetched_text == "":
                        error = "I found the page, but could not read article paragraphs from it."
                except Exception as problem:
                    error = "The article text could not be fetched: " + str(problem)

    return render_template(
        "search.html",
        articles=articles,
        error=error,
        sources=SOURCE_DOMAINS,
        selected_source=selected_source,
        search_text=search_text,
        fetched_text=fetched_text,
        fetched_url=fetched_url,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
