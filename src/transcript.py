from src.download import get_youtube_transcript


def clean_text(text):

    text=text.replace("\n"," ")

    while "  " in text:
        text=text.replace("  "," ")

    return text.strip()



def get_transcript(url):

    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            print("Using captions")

            return clean_text(text)

    except Exception as e:

        print("Captions failed:",e)


    # NEVER attempt audio in cloud SaaS

    return """Transcript unavailable.

This video blocks transcript extraction.

Try:
• Videos with captions enabled
• Educational videos
• Podcasts
• Lectures

This happens because some videos disable AI access.
"""
