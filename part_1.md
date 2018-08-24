# Part 1: Background info - The Web, APIs

Twitter is part of this wonderful thing called the internet. Specifically, Twitter is what people like to call a **Web App**. Most web apps work by communicating with a **client** via an **API** (Application Programming Interface.)

## APIs

APIs are the language of the web, it's how your browser, the **client**, communicates with the Twitter (or any other web app). Developers at Twitter made an API so that other programmers can properly do things on Twitter according to a specific protocol.

For our bot, we're going to use two APIs, the Twitter API and the OpenWeatherMap API.

## Wrappers

We could access the API directly by using HTTP requests; but, using an API wrapper is much, much easier. There are lot's of APIs out there, and a lot of programmers use python. For this reason, a lot of developers have written python libraries that wrap up all those HTTP requests into easy to call functions. These libraries are sometimes called **wrappers**. Thankfully, there are wrappers for the two APIs we're using. Let's install them now. Open up a terminal or command prompt (make sure you have pip) and type this.

```bash
pip install --user tweepy
```

This will install the tweepy library, which is a wrapper for the Twitter API. We also need a wrapper for the OpenWeatherMap API.

```bash
pip install --user pyowm
```

Let's verify this worked. Open up a python shell

```bash
python
```

You should see a new shell pop up on your terminal, now try to import the libraries we just installed.

```python
import tweepy
```

If that worked try importing pyowm as well.

If you have those libraries installed and you have twitter setup, you're ready to make a twitter bot!

[Part 2: The Code](https://github.com/OKStateACM/TwitterBotCodelab/blob/master/part_2.md)
