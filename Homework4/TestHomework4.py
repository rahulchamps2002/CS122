import unittest
import pandas as pd
from textblob import TextBlob

def extract_hashtags(text):
    import re
    return re.findall(r"#(\w+)", text)

def extract_mentions(text):
    import re
    return re.findall(r"@(\w+)", text)

def classify_sentiment(text):
    if not text:
        return "neutral"
    score = TextBlob(text).sentiment.polarity
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    return "neutral"

def calculate_average_engagement(df):
    result = df.groupby('user_id')[['likes', 'shares']].mean()
    result['engagement'] = result['likes'] + result['shares']
    return result


class TestSocialMediaFunctions(unittest.TestCase):

    def test_extract_hashtags(self):
        text = "Loving the #weather and #sunsets at the beach!"
        expected = ["weather", "sunsets"]
        self.assertEqual(extract_hashtags(text), expected)

    def test_extract_mentions(self):
        text = "Big thanks to @john and @doe for the support!"
        expected = ["john", "doe"]
        self.assertEqual(extract_mentions(text), expected)

    def test_classify_sentiment(self):
        self.assertEqual(classify_sentiment("I love this!"), "positive")
        self.assertEqual(classify_sentiment("This is terrible."), "negative")
        self.assertEqual(classify_sentiment("It's okay."), "neutral")

    def test_average_engagement(self):
        data = {
            'user_id': [1, 1, 2],
            'likes': [10, 20, 30],
            'shares': [5, 15, 10]
        }
        df = pd.DataFrame(data)
        result = calculate_average_engagement(df)
        self.assertAlmostEqual(result.loc[1, 'engagement'], 25.0)  # (15 + 10)
        self.assertAlmostEqual(result.loc[2, 'engagement'], 40.0)  # (30 + 10)

if __name__ == '__main__':
    unittest.main()
