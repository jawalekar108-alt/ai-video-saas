from groq import Groq
from config import GROQ_API_KEY

client=Groq(api_key=GROQ_API_KEY)

def groq_summary(text):

    text=text[:8000]

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