import os
import json
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def call_ollama_analysis(content: str):
    # Specialized prompt for the "Scientific Instrument" feel
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Analyze the entry. Return ONLY JSON: sentiment (0-1), topics (list), cognitive_load (string), summary (string)."},
            {"role": "user", "content": content},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content

    # Guard against the known gap: model doesn't always return valid JSON
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Groq returned non-JSON output: {raw[:200]}")

    return raw