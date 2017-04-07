from __future__ import print_function
from requests_oauthlib import OAuth1Session
import webbrowser

import twitter 
from datetime import *
import datetime
import sys


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

# THIS FUNCTION BELONGS TO THE PYTON-TWITTER-LIBRARY  I CHANGED THE FUNCTION TO RETURN A TOUPLE WITH THE INFO
# https://github.com/bear/python-twitter/blob/master/get_access_token.py
def get_access_token(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    print('\nRequesting temp token from Twitter...\n')

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print('I will try to start a browser to visit the following Twitter page '
          'if a browser will not start, copy the URL to your browser '
          'and retrieve the pincode to be used '
          'in the next step to obtaining an Authentication Token: \n'
          '\n\t{0}'.format(url))

    webbrowser.open(url)
    pincode = input('\nEnter your pincode? ')

    print('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    print('''Your tokens/keys are as follows:
        consumer_key         = {ck}
        consumer_secret      = {cs}
        access_token_key     = {atk}
        access_token_secret  = {ats}'''.format(
            ck=consumer_key,
            cs=consumer_secret,
            atk=resp.get('oauth_token'),
            ats=resp.get('oauth_token_secret')))
    return consumer_key, consumer_secret, resp.get('oauth_token'), resp.get('oauth_token_secret')


def enter_giveaway(api, status):
    '''
    Pre: Pass in an API object and a twitter.Status object
    Post: Retweet the tweet, favorite the tweet, and/or follow the user who posted the tweet as necessary
    Purpose: Enter a twitter giveaway based on instructions in the tweet
    '''
    RT = False  # Track if retweeting is necessary
    
    # Convert the twitter.Status object into a string and split it up to enable use of the status id and screen name
    status_string = status.__repr__()
    attributes = status_string.split(',')
    status_id = attributes[0].split('=')
    screen_name = attributes[1].split('=')
    content = attributes[3].split('=')
    text = content[1]
    is_retweet = text[:3]
    
    if is_retweet != "'RT" and is_retweet != '"RT':
    
        # Convert the twitter.Status string from unicode to ascii
        status_str = status_string.encode('ascii', 'ignore')
        status_str = status_str.lower()
        
        # Check and act upon entry requirements of the giveaway
        if ' rt ' in str(status_str):
            RT = True
        if ' rt' in str(status_str):
            RT = True
        if 'retweet' in str(status_str):
            RT = True
            
        if RT == True:
            api.PostRetweet(status_id[1])
        if 'follow' in str(status_str):
            if 'notification' in str(status_str):
                api.CreateFriendship(None, screen_name[1], True)
            else:
                api.CreateFriendship(None, screen_name[1], False)
        if 'favorite' in str(status_str) or 'like' in str(status_str):
            api.CreateFavorite(None, status_id[1])


def custom_filter(user_filter):
    split_filter = user_filter.split(' ')
    size = len(split_filter)
    new_string = ''
    since = input('Find Tweets since (Press enter for default): (yyyy-mm-dd): ')
    until = input('Find Tweets until (Press enter for default): (yyyy-mm-dd): ')
    if since == '':
        since = datetime.datetime.now()
    if until == '':
        until == since + datetime.timedelta(days=3)
    for i in range(size):
        if split_filter[i][0] == '#':
            split_filter[i] = '%23' + split_filter[i][1:]
    i = 0
    while i < size:
        new_string += split_filter[i]
        new_string += '%20'
        i += 1
    query = "l=en&q=Giveaway%20" + str(new_string) + "since%3A" + str(since) + "%20until%3A" + str(until) + "&src=typd&count=100", since, until
    return query


# Create an API object to interact with the Twitter API
if __name__ == "__main__" :
    key = input('Enter your consumer key: ')
    secret = input('Enter your consumer secret: ')
    consumer_key, consumer_secret, access_token_key, access_token_secret = get_access_token(key, secret)
    api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
      
    # print(api.VerifyCredentials())
    today = datetime.datetime.now()
    future_date = today + datetime.timedelta(days=3)
    default_start = {}
    results = {}
    user_filter = str('macbook #film')
    search_custom = custom_filter(user_filter)
    results['Custom Filter'] = search_custom
    search_default = api.GetSearch(
        raw_query="l=en&q=Giveaway%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['default'] = search_default
    search_game = api.GetSearch(
        raw_query="l=en&q=Giveaway%20game%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['game'] = search_game
    search_beauty = api.GetSearch(
        raw_query="l=en&q=Giveaway%20beauty%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['beauty'] = search_beauty
    search_csgo = api.GetSearch(
        raw_query="l=en&q=Giveaway%20csgo%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['csgo'] = search_csgo
    search_stattrak = api.GetSearch(
        raw_query="l=en&q=Giveaway%20StatTrak%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['StatTrak'] = search_stattrak
    search_desktop = api.GetSearch(
        raw_query="l=en&q=Giveaway%20Desktop%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Desktop'] = search_desktop
    search_shirt = api.GetSearch(
        raw_query="l=en&q=Giveaway%20shirt%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['shirt'] = search_shirt
    search_ps4 = api.GetSearch(
        raw_query="l=en&q=Giveaway%20ps4%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['ps4'] = search_ps4
    search_xboxone = api.GetSearch(
        raw_query="l=en&q=Giveaway%20xbox%20one%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Xbox One'] = search_xboxone
    search_pc = api.GetSearch(
        raw_query="l=en&q=Giveaway%20PC%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['pc'] = search_pc
    search_knife = api.GetSearch(
        raw_query="l=en&q=Giveaway%20knife%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Knives'] = search_knife
    search_iphone = api.GetSearch(
        raw_query="l=en&q=Giveaway%20iphone%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['iphone'] = search_iphone
    search_console = api.GetSearch(
        raw_query="l=en&q=Giveaway%20console%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Console'] = search_console
    search_logitech = api.GetSearch(
        raw_query="l=en&q=Giveaway%20logitech%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Logitech'] = search_logitech
    search_nvidia = api.GetSearch(
        raw_query="l=en&q=Giveaway%20Nvidia%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Nvidia'] = search_nvidia
    search_hashtag_giveaway = api.GetSearch(
        raw_query="l=en&q=%23Giveaway%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['#Giveaway'] = search_hashtag_giveaway
    search_itunes = api.GetSearch(
        raw_query="l=en&q=Giveaway%20Itunes%20since%3A" + str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Itunes'] = search_itunes
    search_googleplay = api.GetSearch(
        raw_query="l=en&q=Giveaway%20google%20play%20since%3A" + str(today.year) + "-" + str(today.month)+ "-" + str(today.day) + "%20until%3A" + str(future_date.year) + "-" + str(future_date.month) + "-" + str(future_date.day) + "&src=typd&count=100")
    results['Google Play'] = search_googleplay

    # Enter all tweets found in search above
    for tweet in results['default']:
        try:
            enter_giveaway(api, tweet)
        except twitter.TwitterError:
            pass
