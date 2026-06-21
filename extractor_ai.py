import ollama
import json
import re


def analyze_event(text, url):
    prompt = f"""
You are a professional Thailand BL event verification system.

Your job:
Determine if this text describes a REAL official BL event.

STRICT RULES:
- Only official fan meetings, concerts, press events
- Ignore rumors, comments, fan guesses, ads

Return ONLY valid JSON:

If NOT an event:
{"event": false, "confidence": 0}

If EVENT:

{
  "event": true,
  "confidence": 0-100,
  "company": "",
  "actors": [],
  "date": "YYYY-MM-DD or empty",
  "location": "",
  "ticket_sale": true/false,
  "event_type": "fan_meeting | concert | press | announcement | other",
  "source_quality": "official | news | social | unknown",
  "summary": ""
}

TEXT:
{text[:6000]}
"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response["message"]["content"]

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if not match:
            return {"event": False}

        data = json.loads(match.group())
        data["url"] = url
        return data
    except Exception:
        return {"event": False}