from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def gemini_summary(text):

    try:

        if not text:
            return "No transcript found"

        text = text[:12000]

        prompt = f"""
Create a structured summary.

SUMMARY:
KEY POINTS:
MAIN IDEAS:
ACTION ITEMS:

{text}
"""

        response = client.models.generate_content(

            model="gemini-2.0-flash",

            contents=prompt

        )

        return response.text

    except Exception as e:

        print("Gemini error:", e)

        raise Exception("Gemini failed")
