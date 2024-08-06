from YT_Sentiments.helpers import sentimentScore
from YT_Sentiments.helpers import ytComments

class analyzer:
    """
    Takes <limit> number of comments from the specified video using the api defined in <api> and performs sentiment analysis on them.

    Parameters:

    video_link [string]: full https link of the youtube video
    api [string]: youtube v3 developer api key 
    limit [int]: upper bound of the number of comments

    methods:

    """

    def __init__(self, api, video_link, limit = 600) -> None:
            self.LINK = video_link
            self.LIMIT = limit
            self.API_KEY = api
            self.positive = []
            self.negative = []
            self.neutral = []
            self.polarityList = []
            relevant_comments = ytComments.getComments(self.LINK, self.API_KEY, self.LIMIT)
            for items in relevant_comments:
                polarity = sentimentScore.getSentimentScore(items)
                self.polarityList.append(polarity)
                if polarity["compound"] > 0.05:
                    self.positive.append(items)
                elif polarity["compound"] < -0.05:
                    self.negative.append(items)
                else:
                    self.neutral.append(items)
            
    def get_analysis(self):
        """
        Simply call this on the analyzer object to get a list of comprehensive results.

        Returns:
        a list containing all the positive, negative, neutral comments and the polarities of each comment.
        [positive_list, negative_list, neutral_ist, polarity_list[dict]]

        """
        return [self.positive, self.negative, self.neutral, self.polarityList]
    
    def get_positive(self):
        """
        Simply call this on the analyzer object to get a list of all positive comments.

        Returns:
        a list containing all the positive comments.
        list[string] 
        """
        return self.positive
    
    def get_negative(self):
        """
        Simply call this on the analyzer object to get a list of all negative comments.

        Returns:
        a list containing all the negative comments.
        list[string] 
        """
        return self.negative
    
    def get_neutral(self):
        """
        Simply call this on the analyzer object to get a list of all neutral comments.

        Returns:
        a list containing all the neutral comments.
        list[string] 
        """
        return self.neutral
    
    def get_polarity(self):
        """
        Simply call this on the analyzer object to get a list of all polarities.

        Returns:
        a list containing all the polarities.
        list[dict] 
        """
        return self.polarityList

