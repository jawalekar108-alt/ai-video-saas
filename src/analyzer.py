from groq import Groq

import os

client = Groq(

api_key=os.getenv(

"GROQ_API_KEY"

))

def analyze(text):

    text=text[:12000]

    res=client.chat.completions.create(

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

IMPORTANT IDEAS

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
