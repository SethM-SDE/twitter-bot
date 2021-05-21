#!/usr/bin/env python3

import secrets.secrets as secrets
import requests
import tweepy
import random
from datetime import datetime

# assign variables from secrets to new names
consumer_key = secrets.CONSUMER_KEY
consumer_secret = secrets.CONSUMER_SECRET
access_token = secrets.ACCESS_TOKEN
access_token_secret = secrets.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

# define error log file
ERROR_LOG = 'DadBotLog.txt'

# create easier to manage variable name for tweepy API
tw_api = tweepy.API(auth)


# function to make a tweet
def new_tweet(tweet_body):
    tw_api.update_status(tweet_body)


# function to log errors/exceptions
def log_to_file(api, error):
    # create (if necessary) and append errors to log file
    with open(ERROR_LOG, 'a+') as log_file:
        log_file.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")} API error: {error}')


# joke function to return a random joke from icanhazdadjoke.com
def dad_retriever():
    # dad joke API URL
    url = 'https://icanhazdadjoke.com/'
    # custom headers requested by API developer
    headers = {'User-Agent': 'Twitter bot https://github.SethM-SDE/mycode/pythonproject', 'Accept': 'application/json'}
    # API call
    dad_data = requests.get(url, headers=headers)
    # check for not 200 status
    if dad_data.status_code != 200:
        # log error to file
        log_to_file('Dad Joke API', dad_data.status_code)
    # response conversion
    dad_dict = dad_data.json()
    # create results containing status code and the joke from dad_dict
    results = (dad_data.status_code, dad_dict['joke'])
    # return results
    return results


# friends quote function to return a random friends quote
def friends_retriever():
    # friends quote API URL
    url = 'https://friends-quotes-api.herokuapp.com/quotes/random'
    # API call
    friends_data = requests.get(url)
    # check for non 200 status code
    if friends_data.status_code != 200:
        # log error to file
        log_to_file('Friends Quote API', friends_data.status_code)
    # response conversion
    friends_dict = friends_data.json()
    # format a string for quote and character who said it
    friends_quote = f'\"{friends_dict["quote"]}\" -{friends_dict["character"]}'
    # create results based on status code and the joke
    results = (friends_data.status_code, friends_quote)
    # return custom string
    return results


# Chuck Norris function to return random Chuck Norris joke
def chuck_retriever():
    # Chuck joke API URL (excludes explicit jokes)
    url = 'http://api.icndb.com/jokes/random?exclude=[explicit]'
    # API call
    chuck_data = requests.get(url)
    # check for non 200 status
    if chuck_data.status_code != 200:
        # log error to file
        log_to_file('Chuck Joke API', chuck_data.status_code)
    # response conversion
    chuck_dict = chuck_data.json()
    # create results based on status code and chuck joke
    results = (chuck_data.status_code, chuck_dict['value']['joke'])
    # return joke from dictionary
    return results


# main function definition
def main():
    # length check variable to verify tweet is <= 280 characters
    len_check = True
    # counter to limit checks to 5 in case no internet connection
    tries = 0
    # loops while len_check is true
    while len_check and tries < 5:
        # dictionary of methods that return quotes/jokes
        quotes_dict = {0: dad_retriever(), 1: friends_retriever(), 2: chuck_retriever()}
        # generate random index (0-2)
        idx = random.randint(0, 2)
        # get tweet input from function based on idk variable
        tweet_input = quotes_dict[idx]
        # restart loop in 200 status was not sent from APIs
        if tweet_input[0] != 200:
            tries += 1
            continue
        # publish tweet if character output is <= 208 characters
        if len(tweet_input[1]) <= 280:
            try:
                # create new tweet with tweet input (commented out until full publish)
                new_tweet(tweet_input[1])
            except tweepy.error.TweepError('duplicate tweet'):
                log_to_file('Tweepy', 'duplicate tweet')
                tries += 1
                continue
            # print tweet_input for visual confirmation
            print(tweet_input[1])
            # change len_check to false to break loop
            len_check = False
        else:
            # while loop because tweet was too long
            tries += 1
            continue


if __name__ == '__main__':
    main()
