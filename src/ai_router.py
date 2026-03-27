from src.groq_client import groq_summary
from src.gemini_client import gemini_summary

def generate_summary(text):

    # Try GROQ first (fast)
    try:

        print("Trying Groq")

        return groq_summary(text)

    except Exception as e:

        print("Groq failed:",e)

    # Fallback Gemini
    try:

        print("Trying Gemini")

        return gemini_summary(text)

    except Exception as e:

        print("Gemini failed:",e)

    # Final fallback
    print("Using basic summary")

    return text[:1500]