import os
from groq import Groq

def groq_summary(text):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Groq API key missing"

    if not text:
        return "No transcript available"

    try:

        client = Groq(api_key=api_key)

        text = text[:10000]

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

    except Exception as e:

        return "Summary generation failed"
