from textblob import TextBlob


def main(text):

    s = get_subjectivity(text)

    if s > 0.2:
        print("This sentence is positive.")
    elif s < -0.2:
        print("This sentence is negative.")
    else:
        print("This sentence is neutral.")


def get_subjectivity(text):
    return TextBlob(text).sentiment.polarity
