from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def gemini_summary(text):

    try:

        prompt=f"""

Create:

SUMMARY
KEY TOPICS
IMPORTANT IDEAS
ACTION STEPS
STUDY NOTES

{text[:8000]}

"""

        response = client.models.generate_content(

            model="gemini-1.5-flash",

            contents=prompt

        )

        return response.text

    except Exception as e:

        print("Gemini failed:",e)

        raise Exception("Gemini failed")
