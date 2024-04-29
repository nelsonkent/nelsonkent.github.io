import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")

# Create API object
api = tweepy.API(auth)

# Example: Retrieve tweets from Google's official account
tweets = api.user_timeline(screen_name="Google", count=10, tweet_mode="extended")

for tweet in tweets:
    print(tweet.full_text)
    print("------")
