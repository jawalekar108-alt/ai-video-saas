import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def gemini_summary(text):

    try:

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""

Create:

SUMMARY
KEY TOPICS
IMPORTANT IDEAS
ACTION STEPS
STUDY NOTES

{text[:8000]}

"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print("Gemini error:",e)

        raise Exception("Gemini failed")
