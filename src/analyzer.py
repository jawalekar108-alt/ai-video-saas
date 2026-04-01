from openai import OpenAI

from config import OPENAI_API_KEY


client=

OpenAI(api_key=

OPENAI_API_KEY)


def analyze(text):

    if not text:

        return "Transcript unavailable"

    text=text[:12000]

    try:

        response=

        client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0.3,

        messages=[

        {

        "role":"user",

        "content":

        f"""

Create structured study notes.

SUMMARY
KEY POINTS
IMPORTANT IDEAS
ACTIONABLE TAKEAWAYS

Transcript:

{text}

"""

        }

        ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return str(e)
