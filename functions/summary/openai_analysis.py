import json
import os
import re


_SYSTEM_PROMPT = """You are a media bias analyst specializing in conflict and political reporting.

Your task:
1. Identify the TWO main opposing parties or sides in this article.
2. For EACH party, assess how the article treats them — what language is used, who is given
   agency, who is blamed or victimized, whose perspective is centered.
3. Assign a favorability score to each party based on the article's coverage.
4. Find verbatim quotes that most clearly reveal which party benefits from the framing.

Return ONLY this exact JSON structure — no other text:
{
  "summary": "Factual summary of what the article covers (1-4 sentences, proportional to article length)",
  "parties": [
    {
      "name": "Full descriptive name of party (e.g. Israeli Military / IDF)",
      "description": "Their role in this story in 8-12 words",
      "tone": "favorable",
      "favorability": 0.65,
      "portrayal": "One sentence on how this party is depicted in the article"
    },
    {
      "name": "Full descriptive name of opposing party (e.g. Palestinian civilians / Hamas)",
      "description": "Their role in this story",
      "tone": "unfavorable",
      "favorability": -0.55,
      "portrayal": "One sentence on how this party is depicted"
    }
  ],
  "favored_party": "Name of the party the article favors, or null if coverage is balanced",
  "bias_explanation": "One sentence: which party benefits from the framing and what linguistic choices create that effect",
  "attributed_quotes": [
    {
      "quote": "Exact verbatim text copied from the article",
      "party": "Name of the party this quote affects",
      "impact": "favorable",
      "explanation": "One sentence on why this language helps or hurts this party's image"
    }
  ]
}

Rules:
- parties: exactly 2 entries; list the MORE favorably covered party first
- favorability: float from -1.0 (very unfavorable coverage) to +1.0 (very favorable)
- tone: exactly "favorable", "neutral", or "unfavorable" (lowercase)
- impact: exactly "favorable" or "unfavorable" (lowercase)
- attributed_quotes: COPY-PASTE only — every quote must be a continuous substring that
  exists word-for-word in the article text. If the article is too short or contains no
  quotable framing language, return an empty array []. Never invent or paraphrase.
- Choose quotes that most clearly reveal which party benefits or suffers from the framing
"""


def _is_verbatim(quote, source_text):
    """
    Return True only if the quote is a genuine substring of source_text.
    Normalises whitespace and strips outer quotation marks before comparing,
    so minor whitespace differences don't cause false negatives.
    Requires at least 6 characters to avoid trivially short matches.
    """
    q = re.sub(r'\s+', ' ', quote.strip().strip('"').strip("'")).lower()
    t = re.sub(r'\s+', ' ', source_text).lower()
    return len(q) >= 6 and q in t


def analyze_with_openai(text):
    """
    Returns a dict with:
      summary, parties (bilateral coverage), favored_party, bias_explanation,
      attributed_quotes, spectrum_pct (0-100 CSS position for the bias bar).
    Returns None if the API key is missing/fake or the call fails.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or "fake" in api_key.lower() or api_key.startswith("sk-your"):
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text[:5000]},
            ],
            max_tokens=1000,
        )
        raw = json.loads(response.choices[0].message.content)

        # --- Normalize and compute derived values ---

        for party in raw.get("parties", []):
            party["tone"] = str(party.get("tone", "neutral")).lower().strip()
            if party["tone"] not in ("favorable", "unfavorable", "neutral"):
                party["tone"] = "neutral"

            try:
                fav = float(party.get("favorability", 0))
                party["favorability"] = round(max(-1.0, min(1.0, fav)), 2)
            except (TypeError, ValueError):
                party["favorability"] = 0.0

            # marker_pct: 0% = fully unfavorable, 50% = neutral, 100% = fully favorable
            party["marker_pct"] = round((party["favorability"] + 1) / 2 * 100, 1)

        for q in raw.get("attributed_quotes", []):
            q["impact"] = str(q.get("impact", "unfavorable")).lower().strip()
            if q["impact"] not in ("favorable", "unfavorable"):
                q["impact"] = "unfavorable"

        # Drop any quote that cannot be found verbatim in the original text.
        # This is the hard guard against hallucination — the model sometimes
        # invents plausible-sounding quotes for very short or ambiguous inputs.
        raw["attributed_quotes"] = [
            q for q in raw.get("attributed_quotes", [])
            if _is_verbatim(q.get("quote", ""), text)
        ]

        # Bilateral spectrum: 0% = article fully favors parties[0],
        #                     50% = neutral, 100% = fully favors parties[1]
        parties = raw.get("parties", [])
        if len(parties) >= 2:
            a = parties[0]["favorability"]
            b = parties[1]["favorability"]
            # bias_score: +1 = entirely favors parties[0], -1 = entirely favors parties[1]
            bias_score = (a - b) / 2.0
            raw["spectrum_pct"] = round((1.0 - bias_score) / 2.0 * 100, 1)
        else:
            raw["spectrum_pct"] = 50.0

        return raw

    except Exception:
        return None
