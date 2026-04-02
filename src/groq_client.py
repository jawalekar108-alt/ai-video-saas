import os
from groq import Groq

def groq_summary(text):

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    text=text[:10000]

    res = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        temperature=0.2,

        max_tokens=1200,

        messages=[

            {
            "role":"system",

            "content":"""
Create:

SUMMARY
KEY POINTS
MAIN IDEAS
ACTION ITEMS
"""
            },

            {
            "role":"user",

            "content":text
            }

        ]

    )

    return res.choices[0].message.content
