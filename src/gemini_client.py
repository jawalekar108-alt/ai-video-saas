from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def gemini_summary(text):

    try:

        text=text[:10000]

        prompt=f"""

Create:

SUMMARY
KEY TOPICS
IMPORTANT IDEAS
ACTION STEPS

{text}

"""

        response = client.models.generate_content(

            model="gemini-2.0-flash",

            contents=prompt

        )

        return response.text

    except:

        raise Exception("Gemini failed")
