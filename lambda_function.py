import tweepy
import random
from KEYS import *

def lambda_handler(event, context):

	# Authenticate to Twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

	# Pick a random quote from a text file
	textfile = open("frankenbot.txt", "r")
	quotes = textfile.read().splitlines()
	onequote = random.choice(quotes)

	textfile.close()
	
	# Create API object
	api = tweepy.API(auth)

	# Create a tweet
	status = api.update_status(onequote)
	
	return