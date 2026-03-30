
import os
from openai import OpenAI


def analyze(text):

    if not text:

        return "Transcript unavailable"


    # Prevent token overflow
    text=text[:12000]


    api_key=os.getenv("OPENAI_API_KEY")

    if not api_key:

        return "OpenAI API key missing"


    try:

        client=OpenAI(api_key=api_key)


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





# from groq import Groq
# from config import GROQ_API_KEY

# client = Groq(api_key=GROQ_API_KEY)

# def analyze(text):

#     if not text or len(text) < 50:
#         return "Transcript too short to analyze."

#     text = text[:12000]

#     try:

#         response = client.chat.completions.create(

#             model="llama-3.1-8b-instant",

#             temperature=0.2,

#             max_tokens=1500,

#             messages=[

#                 {
#                 "role":"system",

#                 "content":"""

# Analyze transcript and create:

# SUMMARY

# KEY TOPICS

# IMPORTANT IDEAS

# ACTION STEPS

# CHAPTERS

# KEY QUOTES

# STUDY NOTES

# Return clean markdown sections.
# """
#                 },

#                 {
#                 "role":"user",

#                 "content":text
#                 }

#             ]

#         )

#         return response.choices[0].message.content

#     except Exception as e:

#         return f"Analysis failed: {str(e)}"
