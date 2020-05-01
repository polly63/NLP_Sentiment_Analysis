import tweepy
import pandas as pd
from tweepy import OAuthHandler


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

    def get_tweets(self, query, count):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['date'] = tweet.created_at
                parsed_tweet['author'] = tweet.user.name
                parsed_tweet['text'] = tweet.text
                parsed_tweet['number_of_likes'] = tweet.favorite_count
                parsed_tweet['number_of_retweets'] = tweet.retweet_count
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def get_df(query, limit):
    a = 100
    frames = []
    while a <= limit:
        api = TwitterClient()
        tweets = api.get_tweets(query=query, count=limit)
        df = pd.DataFrame(tweets)
        df.index = range(a-100, a)
        frames.append(df)
        a += 100
    result = pd.concat(frames)
    return result


