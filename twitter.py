from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import pyowm
import json
import account_info as info

owm = pyowm.OWM(info.owm_token)
auth = tweepy.OAuthHandler(info.ckey, info.csecret)
auth.set_access_token(info.atoken, info.asecret)
api = tweepy.API(auth)

def send_tweet(username, tweetID, temp):
    tweet = "@{} The weather in Stillwater, OK is currently {} degrees.".format(username, username, temp)
    api.update_status(tweet, tweetID)


class Listener(StreamListener):

    def on_data(self, data):
        tweet_data = json.loads(data)
        from_self = tweet_data.get('user', {}).get('id_str', '') == info.user_id

        if not from_self:
            id = tweet_data["id"]
            username = tweet_data["user"]["screen_name"]
            observation = owm.weather_at_id(4552215)
            weather = observation.get_weather()
            tempature = weather.get_temperature('fahrenheit')['temp']
            send_tweet(username,id,tempature)
            return (True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(info.ckey, info.csecret)
auth.set_access_token(info.atoken, info.asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@emayberry74"])
