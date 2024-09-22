
import tweepy
import os
import schedule
import time

# os.environ['http_proxy'] = 'http://127.0.0.1:7078'
# os.environ['https_proxy'] = 'http://127.0.0.1:7078' 

consumer_key = "kRFb29wGXKUZ2RMMfPRkNxeBG"
consumer_secret = "BEwF0htC4ENMnRS7kk6qxh2Qj4Pn0T0wWzXlhMNjTYor7YDRGE"
access_token = "1751258845177884672-ABpGHC6tGKLeVs8mqFt0aaCLvnNNZh"
access_token_secret = "BB6xluysba9GbMQ8reyVyMZNXPqLzuiHectV6E4gw2TcM"

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)


# Create Tweet

def job_create_twitter():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    response = client.create_tweet(
       text="This Tweet was Tweeted using Tweepy and Twitter API v2 " + now + ".")
    print(now + f" https://twitter.com/user/status/{response.data['id']}")

schedule.every(3).seconds.do(job_create_twitter)

while True:
    schedule.run_pending()
    time.sleep(1)
