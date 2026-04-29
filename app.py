import json
import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, render_template, request, session, url_for

from analysis_pipeline import analyze_article, compare_articles
from functions.article_sources.gdelt_source import (
    SOURCE_DOMAINS,
    fetch_article_text,
    search_articles,
)
import database

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")

# Ensure the SQLite DB and table exist on startup
database.init_db()


def build_article_from_form(letter):
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


# ── Analysis page ────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    article_a = None
    article_b = None
    comparison = None
    error = ""

    preload_a = session.pop("preload_a", None)
    preload_b = session.pop("preload_b", None)

    mode = "compare" if preload_b else "single"

    if request.method == "POST":
        mode = request.form.get("mode", "single")
        article_a = build_article_from_form("a")

        if mode == "compare":
            article_b = build_article_from_form("b")

        if article_a is None and article_b is None:
            error = "Paste text into at least one article box before analyzing."

        if mode == "compare" and article_a is not None and article_b is not None:
            comparison = compare_articles(article_a, article_b)

    return render_template(
        "index.html",
        article_a=article_a,
        article_b=article_b,
        comparison=comparison,
        error=error,
        sources=SOURCE_DOMAINS,
        mode=mode,
        preload_a=preload_a,
        preload_b=preload_b,
    )


# ── Load article from search into analysis form ──────────────
@app.route("/load_article", methods=["POST"])
def load_article():
    slot = request.form.get("slot", "a")
    session["preload_" + slot] = {
        "title": request.form.get("title", ""),
        "source": request.form.get("source", ""),
        "text": request.form.get("text", ""),
    }
    return redirect(url_for("index"))


# ── Save analysed article to collection ─────────────────────
@app.route("/save_article", methods=["POST"])
def save_article():
    title = request.form.get("title", "").strip() or "Untitled"
    source = request.form.get("source", "").strip()
    tags_raw = request.form.get("tags", "").strip()
    ai_json = request.form.get("ai_analysis_json", "")
    compound = request.form.get("sentiment_compound", "0")
    label = request.form.get("sentiment_label", "")
    framing = request.form.get("framing_ratio", "0")

    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    if not tags:
        tags = ["untagged"]

    try:
        ai_analysis = json.loads(ai_json) if ai_json else None
    except (json.JSONDecodeError, ValueError):
        ai_analysis = None

    database.save_article(
        title=title,
        source=source,
        tags=tags,
        ai_analysis=ai_analysis,
        sentiment_compound=float(compound) if compound else 0.0,
        sentiment_label=label,
        framing_ratio=float(framing) if framing else 0.0,
    )

    first_tag = tags[0]
    return redirect(url_for("collection", tag=first_tag, saved=title))


# ── Collection & tag comparison ──────────────────────────────
@app.route("/collection")
def collection():
    tags = database.all_tags()
    selected_tag = request.args.get("tag", "")
    saved_title = request.args.get("saved", "")
    articles = database.articles_by_tag(selected_tag) if selected_tag else []
    return render_template(
        "collection.html",
        tags=tags,
        selected_tag=selected_tag,
        articles=articles,
        saved_title=saved_title,
    )


@app.route("/collection/delete/<int:article_id>", methods=["POST"])
def delete_article(article_id):
    tag = request.form.get("tag", "")
    database.delete_article(article_id)
    return redirect(url_for("collection", tag=tag))


# ── Article search ───────────────────────────────────────────
@app.route("/search", methods=["GET", "POST"])
def search():
    articles = []
    error = ""
    selected_source = "The Guardian"
    search_text = ""
    fetched_text = ""
    fetched_url = ""
    fetched_title = ""
    fetched_domain = ""

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

        elif action == "fetch":
            fetched_url = request.form.get("article_url", "").strip()
            fetched_title = request.form.get("article_title", "").strip()
            fetched_domain = request.form.get("article_domain", "").strip()

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
        fetched_title=fetched_title,
        fetched_domain=fetched_domain,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
