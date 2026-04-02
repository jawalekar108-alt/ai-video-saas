from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def summarize(text):

    try:

        text = text[:15000]

        prompt = f"""
        Create a structured summary:

        1 Key points
        2 Main ideas
        3 Short summary

        Transcript:
        {text}
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return "Summary generation failed. Try another video."
