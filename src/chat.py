import os
from groq import Groq


def ask_video(question,transcript):

    api_key=os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Groq API key missing"

    if not transcript:
        return "Transcript missing"

    try:

        client=Groq(api_key=api_key)

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

                    "content":f"""

Transcript:
{context}

Question:
{question}

"""
                }

            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Question failed: {str(e)}"
