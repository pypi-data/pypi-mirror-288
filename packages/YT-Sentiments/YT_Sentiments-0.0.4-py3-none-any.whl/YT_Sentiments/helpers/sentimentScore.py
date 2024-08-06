from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def getSentimentScore(comment):
    """
    Takes a single string comment and gets the polarity score of the comment

    Parameters:

    comment [string]: the comment to be analyzed


    Returns:
 
    sentiment [dict]: a dict conatining key-value pair of neg, neu, pos, and compound scores
    """

    # Creating a SentimentIntensityAnalyzer object.
    sentiment_object = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment_object.polarity_scores(comment)

    return sentiment_dict