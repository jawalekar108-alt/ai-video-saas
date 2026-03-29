from src.groq_client import groq_summary
from src.gemini_client import gemini_summary

def generate_summary(text):

    try:

        return groq_summary(text)

    except Exception as e:

        print("Groq failed:",e)

    try:

        return gemini_summary(text)

    except Exception as e:

        print("Gemini failed:",e)

    return text[:1500]
