import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def summarize(text):

    prompt = f"""
    Summarize this YouTube transcript clearly:

    {text[:12000]}
    """

    response = model.generate_content(prompt)

    return response.text
