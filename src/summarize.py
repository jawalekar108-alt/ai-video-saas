from groq import Groq
from config import GROQ_API_KEY
import time

client=Groq(api_key=GROQ_API_KEY)

def summarize_text(text):

    print("Generating final summary")

    res=client.chat.completions.create(

        model="llama-3.1-8b-instant",

        temperature=0.2,

        max_tokens=900,

        messages=[

        {

        "role":"system",

        "content":"""

Create:

SUMMARY
KEY POINTS
INSIGHTS
ACTION ITEMS

Be concise.
"""

        },

        {

        "role":"user",

        "content":text[:12000]

        }

        ]

    )

    time.sleep(8)

    return res.choices[0].message.content


def extract_highlights(text):

    sentences=text.split(".")

    important=[s.strip() for s in sentences if len(s)>100]

    return important[:15]