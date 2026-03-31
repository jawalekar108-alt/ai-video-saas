import os
from openai import OpenAI


def analyze(text):

    if not text:
        return "Transcript unavailable"

    text=text[:12000]

    api_key=os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "OpenAI API key missing"

    try:

        client=OpenAI()

        prompt=f"""
Create structured study notes from this video transcript.

Format exactly like this:

SUMMARY:
(short paragraph)

KEY POINTS:
• point
• point
• point

IMPORTANT IDEAS:
• idea
• idea

ACTIONABLE TAKEAWAYS:
• takeaway
• takeaway

Transcript:
{text}
"""

        response=client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            temperature=0.3

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI analysis failed: {str(e)}"
