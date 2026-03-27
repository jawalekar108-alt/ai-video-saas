from groq import Groq
from config import GROQ_API_KEY

client=Groq(api_key=GROQ_API_KEY)

def ask_video(question,transcript):

    context=transcript[:8000]

    response=client.chat.completions.create(

    model="llama-3.1-8b-instant",

    temperature=0.3,

    max_tokens=500,

    messages=[

    {

    "role":"system",

    "content":"Answer questions from transcript"

    },

    {

    "role":"user",

    "content":

    f"""

Transcript:

{context}

Question:

{question}

"""

    }

    ]

    )

    return response.choices[0].message.content