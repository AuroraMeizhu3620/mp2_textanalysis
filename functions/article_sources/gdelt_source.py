import json
import re
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


SOURCE_DOMAINS = {
    "The Guardian": "theguardian.com",
    "BBC": "bbc.com",
    "NPR": "npr.org",
    "Reuters": "reuters.com",
    "Associated Press": "apnews.com",
}


def search_articles(search_text, source_name, max_results=5):
    """
    Search GDELT for articles from one source.

    GDELT is useful for a beginner project because it does not require an API key.
    It usually gives article links and short metadata, not guaranteed full text.
    """
    domain = SOURCE_DOMAINS.get(source_name, "")
    query = search_text.strip()

    if domain != "":
        query = query + " domain:" + domain

    url = (
        GDELT_URL
        + "?query="
        + quote_plus(query)
        + "&mode=artlist&format=json&maxrecords="
        + str(max_results)
    )

    request = Request(url, headers={"User-Agent": "mp2-text-analysis-student-app"})

    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    articles = []

    for article in data.get("articles", []):
        articles.append(
            {
                "title": article.get("title", "Untitled article"),
                "url": article.get("url", ""),
                "domain": article.get("domain", ""),
                "date": article.get("seendate", ""),
            }
        )

    return articles


class ParagraphParser(HTMLParser):
    """Very small HTML parser that keeps text from paragraph tags."""

    def __init__(self):
        super().__init__()
        self.inside_paragraph = False
        self.paragraphs = []
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.inside_paragraph = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "p" and self.inside_paragraph:
            clean_text = self.current_text.strip()

            if len(clean_text) > 40:
                self.paragraphs.append(clean_text)

            self.inside_paragraph = False

    def handle_data(self, data):
        if self.inside_paragraph:
            self.current_text += " " + data


def fetch_article_text(article_url):
    """
    Try to fetch readable paragraph text from an article URL.

    Some news websites block automatic fetching. When that happens, the app
    tells the user to paste the article text instead.
    """
    request = Request(article_url, headers={"User-Agent": "mp2-text-analysis-student-app"})

    with urlopen(request, timeout=10) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = ParagraphParser()
    parser.feed(html)
    article_text = "\n\n".join(parser.paragraphs)

    article_text = re.sub(r"\s+", " ", article_text).strip()
    return article_text
