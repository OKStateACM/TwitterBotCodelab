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

This class has two methods in it, ```on_data```, and ```on_error```. They are empty right now (which is why the body has ```pass``` in it.
