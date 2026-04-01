def analyze(text):

    if not text:

        return "No content"

    words=text.split()

    summary=" ".join(words[:200])

    notes=f"""

KEY POINTS:

{summary}

VIDEO LENGTH WORDS:
{len(words)}

"""

    return notes
