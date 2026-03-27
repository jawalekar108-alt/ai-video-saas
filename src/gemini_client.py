from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def gemini_summary(text):

    text=text[:8000]

    prompt=f"""

Analyze transcript and create:

SUMMARY
KEY POINTS
ACTION STEPS

{text}

"""

    response=client.models.generate_content(

    model="gemini-1.5-flash",

    contents=prompt

    )

    return response.text

def gemini_summary(text):

    text=text[:8000]

    prompt=f"""

Analyze transcript and create:

SUMMARY
KEY POINTS
ACTION ITEMS

{text}

"""

    res=model.generate_content(prompt)

    return res.text