import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze(text):
    prompt = f"""
    Summarize this YouTube video clearly:

    {text[:4000]}
    """

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
