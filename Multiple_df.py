import tweepy
import pandas as pd
import nltk
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        consumer_key = 'BYecfzPaN4XZBRaHKdQmz3w5Y'
        consumer_secret = 'nOGwDgHxudwGvBHRVORutMmj38i3uhJ5nLJekaeJPId9PJZPbR'
        access_token = '1063194642760445952-ZL82gfVMrnAcQ23MpKnEnQ93LnNNyB'
        access_token_secret = 'gpaH2Cp0H7qgUKCuMaj4RUTzd7bEPWK5BXL8cGvUw4zdk'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query: str, count: int):
        """
        Search query in the tweet api and return the result.
        count max is 100.
        """
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def get_df(query: str, limit: int):
    """
    Return the dataframe after you search the query.
    Limit: the number of tweet you want to search.
    """
    a = 100
    frames = []
    while a <= limit:
        api = TwitterClient()
        tweets = api.get_tweets(query=query, count=100)
        df = pd.DataFrame(tweets)
        frames.append(df)
        a += 100
    df = pd.concat(frames, ignore_index=True)
    return df


def get_mul_df(keywords: dict, limit: int):
    """
    Search every string of every dictionary key and return multiple dataframe corresponding to each key.
    """
    df_set = []
    for key in keywords:
        strings_set = []
        strings_list = []
        for strings in keywords[key]:
            strings_list.append(strings)
            strings_set.append(get_df(strings, limit))
        result = pd.concat(strings_set, keys=strings_list)
        df_set.append(result)
    return df_set


def tag_keywords(keywords: dict, limit: int):
    """
    POS tag for the tweets searched for each string of every dictionary key and return the result.
    """
    df = get_mul_df(keywords, limit)
    i = 0
    j = 0
    word_list = []
    while j < len(df):
        while i < len(df[j].text):
            text = nltk.word_tokenize(df[j].text[i])
            word_list.append(nltk.pos_tag(text))
            i += 1
        i = 0
        j += 1
    return word_list


def get_tweet_sentiment(keywords: dict, limit: int):
    """
    Sentiment Analysis for each string of each dictionary key. Return a dictionary with key and the
    corresponding result.
    Example: get_tweet_sentiment({'apple': ['total', 'sale'], 'google': ['can', 'be']}, 200)
    """
    whole = {}
    for keys in keywords:
        whole_list = []
        for strings in keywords[keys]:
            df = get_df(strings, limit)
            i = 0
            sentiment_list = []
            while i < len(df):
                analysis = TextBlob(df.text[i])
                if analysis.sentiment.polarity > 0:
                    sentiment_list.append('positive')
                elif analysis.sentiment.polarity == 0:
                    sentiment_list.append('neutral')
                else:
                    sentiment_list.append('negative')
                i += 1
            whole_list.append(sentiment_list)
        whole[keys] = whole_list
    return whole


def positive_percent(keywords: dict, limit: int):
    """
    Return the dictionary with each key and corresponding percent of positive words.\
    >> a = {'apple': ['total', 'sale'], 'google': ['can', 'be']}
    >> positive_percent(a, 300)
    {'apple': [0.24083769633507854, 0.19230769230769232], 'google': [0.3904109589041096, 0.38831615120274915]}
    """
    df = get_tweet_sentiment(keywords, limit)
    total = {}
    for key in df:
        positive_list = []
        for items in df[key]:
            index = 0
            for string in items:
                if string == 'positive':
                    index += 1
            percent = index / len(items)
            positive_list.append(percent)
        total[key] = positive_list
    return total


