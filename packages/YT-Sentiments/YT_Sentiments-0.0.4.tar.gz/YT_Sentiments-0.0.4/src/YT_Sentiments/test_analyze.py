import unittest
from sentiment import analyzer
from helpers import sentimentScore
class test_analyze(unittest.TestCase):

    #assert sum of all comments equals the sum of scores in polarity
    def test_get_analysis(self):
        obj = analyzer(api = input("please enter your Youtube API_KEY: "), video_link = "https://www.youtube.com/watch?v=hql6doE-Ccw", limit=100)
        result = obj.get_analysis()
        sum = len(result[0])+len(result[1])+len(result[2])
        self.assertEqual(sum, len(result[3]))

    #assert precense of certain keys in the result dict
    def test_get_score(self):
        comments = ["Absolutely worth every penny", "Still the best PC gaming handheld on the market", "just some marketing gimmick."]
        expected_keys = {"neg", "neu", "pos", "compound"}
        for comment in comments:
            polarity = sentimentScore.getSentimentScore(comment)
            assert expected_keys.issubset(polarity.keys())
            

if __name__ == '__main__':
    unittest.main()