import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------- TEMPORARY DIAGNOSTIC ----------
# This prints a masked version of the key so we can confirm
# it is actually being loaded from .env without exposing it.
if GEMINI_API_KEY:
    print(f"\n[DEBUG] GEMINI_API_KEY loaded. Length={len(GEMINI_API_KEY)}, "
          f"starts_with='{GEMINI_API_KEY[:6]}...', ends_with='...{GEMINI_API_KEY[-4:]}'\n")
else:
    print("\n[DEBUG] GEMINI_API_KEY is None — .env was not found or variable name is wrong.\n")
# -------------------------------------------

# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


def analyze_lyrics(lyrics):

    prompt = f"""
You are a professional music expert.

Analyze the following song lyrics.

Lyrics:
{lyrics}

Return ONLY valid JSON.

Use this exact structure:

{{
    "title": "",
    "artist": "",
    "album": "",
    "release_year": "",
    "genre": "",
    "mood": "",
    "emotion": "",
    "theme": "",
    "language": "",
    "keywords": [],
    "confidence": "",
    "summary": ""
}}

Rules:
- Return ONLY JSON.
- No markdown.
- No explanation.
- Unknown values should be "Unknown".
"""

    try:

        print("\n========== Sending Request ==========\n")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        print("\n========== RAW RESPONSE ==========")
        print(text)
        print("==================================\n")

        # Remove Markdown if Gemini returns it
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        try:
            data = json.loads(text)
            return data

        except json.JSONDecodeError:

            print("JSON Parsing Failed. Returning raw response.")

            return {
                "title": "Unknown",
                "artist": "Unknown",
                "album": "Unknown",
                "release_year": "Unknown",
                "genre": "Unknown",
                "mood": "Unknown",
                "emotion": "Unknown",
                "theme": "Unknown",
                "language": "Unknown",
                "keywords": [],
                "confidence": "0%",
                "summary": text
            }

    except Exception as e:

        import traceback

        print("\n========== GEMINI ERROR ==========")
        traceback.print_exc()
        print("==================================\n")

        return {
            "title": "Unavailable",
            "artist": "Unavailable",
            "album": "Unavailable",
            "release_year": "Unavailable",
            "genre": "Unavailable",
            "mood": "Unavailable",
            "emotion": "Unavailable",
            "theme": "Unavailable",
            "language": "Unavailable",
            "keywords": [],
            "confidence": "0%",
            "summary": str(e)
        }