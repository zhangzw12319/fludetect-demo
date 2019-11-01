from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile

# oath = credsfromfile()
# client = Query(**oath)
# tweets = client.search_tweets(keywords='flu, US', limit=5)
# tweet_content = next(tweets)
# from pprint import pprint
# pprint(tweet_content, depth=1)

def get_live_twitter_data():
    tw = Twitter()
    tw.tweets(keywords='flu, health, illness, hospital', stream=False, limit=5, to_screen=False)  #sample from the public stream

# def get_live_twitter_data():
    # oath = credsfromfile()
    # client = Streamer(**oath)
    # client.register(TweetWriter( limit=20))
    # client.filter(track='have a fever, flu')