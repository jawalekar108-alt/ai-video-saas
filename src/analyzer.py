from src.ai_router import generate_summary

def analyze(text):

    if not text or len(text) < 50:

        return "Transcript too short to analyze."

    text=text[:10000]

    try:

        result=generate_summary(text)

        if not result:

            return "Analysis could not be generated."

        return result

    except Exception as e:

        print("Analysis error:",e)

        # final safety fallback
        return text[:1500]
















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