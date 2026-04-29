import os


def summarize_article(text):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or "fake" in api_key.lower() or api_key == "sk-your-openai-api-key-here":
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize the following news article in 3-4 sentences. "
                        "Be concise, factual, and neutral."
                    ),
                },
                {"role": "user", "content": text[:4000]},
            ],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
