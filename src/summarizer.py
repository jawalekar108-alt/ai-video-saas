from transformers import pipeline

summarizer = None


def load_model():

    global summarizer

    if summarizer is None:

        summarizer = pipeline(

            "summarization",

            model="sshleifer/distilbart-cnn-12-6"

        )

    return summarizer


def summarize(text):

    try:

        model = load_model()

        max_chunk = 1000

        chunks = [

            text[i:i+max_chunk]

            for i in range(0,len(text),max_chunk)

        ]

        final_summary=""

        for chunk in chunks:

            result=model(

                chunk,

                max_length=150,

                min_length=40,

                do_sample=False

            )

            final_summary+=result[0]['summary_text']+" "

        return final_summary

    except Exception as e:

        print("Summary failed:",e)

        return None
