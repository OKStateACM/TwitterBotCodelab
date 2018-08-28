# Part 2: The Code

## Account Info

In order to use the Twitter and OpenWeatherMap API, you'll need to define a few things for authorization purposes. Go ahead and create a new python file called ```account_info.py``` and copy this code into it

```python
# Twitter Stuff
ckey = "your_consumer_key"
csecret = "your_consumer_secret"
atoken = "your_access_token"
asecret = "your_access_secret"

# OpenWeatherMap Stuff
owm_token = "your_owm_token"
user_id = "your_user_id"
```

This is just defining a bunch of string variables that we will use in our actual program later. You can go ahead and close that file, we won't be using it again.

## Setting up the Wrappers

Now we can start writing the code for the actual Twitter bot. Create a new file called ```bot.py```

The first thing we'll do is import the python modules that will allow us to do several useful things.

```python
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import pyowm
import json
import account_info as info
```

* You already know what tweepy and pyowm are for, that's how we'll interact with the Twitter and OpenWeatherMap APIs.

* ```json``` is a library that allows us to easily work with JSON formatted data. JSON is just a format for structuring data that's sent between computers.

* ```account_info``` is the module that we just made that contains all of our authentication info!

Now that we have these imported, let's set up some variables that we will use to query OpenWeatherMap and send tweets to Twitter.

```python
owm = pyowm.OWM(info.owm_token)
auth = tweepy.OAuthHandler(info.ckey, info.csecret)
auth.set_access_token(info.atoken, info.asecret)
api = tweepy.API(auth)
```

The two important things here are ```api```, which is how we'll interact with Twitter, and ```owm```, which is how we'll interact with OpenWeatherMap. Notice that we passed in the info from ```account_info``` when we created these. If we didn't do that, it wouldn't work because we wouldn't be authenticated.

If you're new to programming, you might be wondering how we knew how to make those variables. The answer is simple, we looked it up. Documentation is your friend.

## Creating a class that listens and responds to tweets

We're going to create a class called Listener that will listen for tweets and, eventually, respond to them. For those not yet familiar with object oriented programming, a class is a structure that defines how we can make objects to do things. If you're in CS1 currently, you'll learn all about them eventually. For now, hopefully the code is intuitive enough.

```python
class Listener(StreamListener):

    def on_data(self, data):
	pass

    def on_error(self, status):
	pass

```

This class has two methods in it, ```on_data```, and ```on_error```. They are empty right now (which is why the body has ```pass``` in it.)

### ```on_error```

The easiest of these methods to fill out is ```on_error```, this defines what our listener should do when there's an error. Let's simply have it print out the error.

```python
def on_error(self, status):
    print(status)
```

### ```on_data```

The next method we'll fill out is ```on_data```, this is the function that is called whenever our listener "hears" a tweet. Notice that one of the parameters of the function is ```data```. This is just a string, but it represents a **JSON** object. **JSON** stands for Javascript Object Notation and it is a very common method for sending data between a client and a server. For now let's just print it out to see what it looks like.

```python
def on_data(self, data):
    print(data)
```

But in order for this to actually print out, we need to test this! At the very bottom of the file (below the class definition) write this code, replacing "@username" with your twitter username (or your bots username)

```python
twitterStream = Stream(auth, Listener())
twitterStream.filter(track=["@username"])
```

Again, this code may look confusing, but it's all a matter of looking at documentation to figure out how this works. This just creates a new ```Stream``` object called ```twitterStream```, we pass in a new instance of our ```Listener``` class to this stream so our bot knows how to react when it sees a tweet. We then call the ```twitterStream.filter``` function so that it filters out tweets that don't have your username in it (otherwise we'd be flooded with every tweet being tweeted right now, which is a lot.) Passing in ```track=["@username"]``` tells the stream what to look for in the tweets, we only want to see the tweets that mention our username.

## First test

Ok now we're ready to test, open up a terminal and navigate to the directory with your code in it.

```bash
python bot.py
```

Now, making sure to mention your username, tweet something! You should see a large string pop up on your terminal. Looks complicated right? We need to figure out what to do with this.

## Processing ```data```
We can use the ```json``` library we imported earlier to convert the json string into a python dictionary. If you're not familiar with python, a dictionary is basically like a hashmap. If you're new to programming and aren't sure what a hashmap is, don't worry, it's basically just something that maps **keys** to **objects**, so for example we might have a key ```username``` that maps to an object ```@okstateacm```.

```python
def on_data(self, data):
    tweet_data = json.loads(data)
```

This converts the JSON string into a python dictionary so that it's much easier to extract things like usernames. One thing we want to do is check to make sure we're not responding to ourselves. Bots responding to bots can create an infinite loop, which is very bad and can get you kicked off of twitter.

```python
def on_data(self, data):
    tweet_data = json.loads(data)
    from_self = tweet_data.get('user', {}).get('id_str', '') == info.user_id
    
    if not from_self:
        # process the tweet and respond
```

All we did here was create a boolean variable called ```from_self``` that is True if the tweet is from ourselves, and False otherwise. You may not understand exactly how we got that variable, but it's all just a matter of being familiar with python and looking at documentation. We're going to use an if statement to make sure this is False before processing the tweet.

## Processing the Tweet
Now we need to process the tweet, since ```data``` is a python ditionary, this is easy.

```python
def on_data(self, data):
    tweet_data = json.loads(data)
    from_self = tweet_data.get('user', {}).get('id_str', '') == info.user_id
    
    if not from_self:
        id = tweet_data['id'] # Getting the tweet id (we'll need this when we respond to the tweet)
        username = tweet_data['user']['screen_name'] # Getting the username of who tweeted at us
        observation = owm.weather_at_id(4552215) # 4552215 is the id for Stillwater
        weather = observation.get_weather()
        temperature = weather.get_temperature('fahrenheit')['temp']
        return True
```

Now that we have the tweet id, username, and temperature, we can prepare a tweet to send out. We could do this in this function, but let's make another one. Above the class definition, add this function.

```python
def send_tweet(username, tweetID, temp):
    tweet = "@{} The weather in Stillwater, OK is currently {} degrees.".format(username, username, temp)
    api.update_status(tweet, tweetID)
```

All this function does is take the username, tweetID, and temperature and prepare a string to tweet out. Then we call ```api.update_status(tweet, tweetID)``` to actually tweet out the tweet.

Now we can call this function is ```on_data```

```python
def on_data(self, data):
    tweet_data = json.loads(data)
    from_self = tweet_data.get('user', {}).get('id_str', '') == info.user_id
    
    if not from_self:
        id = tweet_data['id'] # Getting the tweet id (we'll need this when we respond to the tweet)
        username = tweet_data['user']['screen_name'] # Getting the username of who tweeted at us
        observation = owm.weather_at_id(4552215) # 4552215 is the id for Stillwater
        weather = observation.get_weather()
        temperature = weather.get_temperature('fahrenheit')['temp']
        send_tweet(username, id, temperature)
        return True
```

## Final Test!

Our twitter bot should be ready now! Run the program by calling ```python bot.py``` and then tweet something to your bot. It should respond with the temperature in Stillwater!

[Part 3: Where to go from here]()
