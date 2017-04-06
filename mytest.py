import twitter 
from datetime import *
import datetime


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
            api.CreateFriendship(None, screen_name[1])
        if 'favorite' in str(status_str) or 'like' in str(status_str):
            api.CreateFavorite(None, status_id[1])


def custom_filter(user_filter):
    split_filter = user_filter.split(' ')
    size = len(split_filter)
    new_string = ''
    since = raw_input('Find Tweets since (Press enter for default): (yyyy-mm-dd): ')
    until = raw_input('Find Tweets until (Press enter for default): (yyyy-mm-dd): ')
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
    query = "l=en&q=Giveaway%20" + new_string + "since%3A" + since + "%20until%3A" + until + "&src=typd&count=100"
    return query


# Create an API object to interact with the Twitter API
api = twitter.Api(
    consumer_key = 'cfNpeV5za47PJBmjm9GrjoQ3F',
    consumer_secret = 'rxIa3R1nwPQSOwSHMCwlE0xOGfHqrDSnsvqJMFPFnnLc2CpXQA',
    access_token_key = '737864657659105280-fJpSG7fDSMW77jCBAmDMEkhpWBReRz8',
    access_token_secret = 'LQjiiaKLRKeXFR6Ew0aaSIsSgb2CczPLIox9rG9FjA5ea'
)
      
# print(api.VerifyCredentials())

today = datetime.datetime.now()
future_date = today + datetime.timedelta(days=3)
default_start =
results = {}
user_filter = 'macbook #film'
search_custom = custom_filter(user_filter)
results['Custom Filter'] = search_custom
search_default = api.GetSearch(
    raw_query="l=en&q=Giveaway%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['default'] = search_default
search_game = api.GetSearch(
    raw_query="l=en&q=Giveaway%20game%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['game'] = search_game
search_beauty = api.GetSearch(
    raw_query="l=en&q=Giveaway%20beauty%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['beauty'] = search_beauty
search_csgo = api.GetSearch(
    raw_query="l=en&q=Giveaway%20csgo%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['csgo'] = search_csgo
search_stattrak = api.GetSearch(
    raw_query="l=en&q=Giveaway%20StatTrak%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['StatTrak'] = search_stattrak
search_desktop = api.GetSearch(
    raw_query="l=en&q=Giveaway%20Desktop%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Desktop'] = search_desktop
search_shirt = api.GetSearch(
    raw_query="l=en&q=Giveaway%20shirt%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['shirt'] = search_shirt
search_ps4 = api.GetSearch(
    raw_query="l=en&q=Giveaway%20ps4%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['ps4'] = search_ps4
search_xboxone = api.GetSearch(
    raw_query="l=en&q=Giveaway%20xbox%20one%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Xbox One'] = search_xboxone
search_pc = api.GetSearch(
    raw_query="l=en&q=Giveaway%20PC%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['pc'] = search_pc
search_knife = api.GetSearch(
    raw_query="l=en&q=Giveaway%20knife%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Knives'] = search_knife
search_iphone = api.GetSearch(
    raw_query="l=en&q=Giveaway%20iphone%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['iphone'] = search_iphone
search_console = api.GetSearch(
    raw_query="l=en&q=Giveaway%20console%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Console'] = search_console
search_logitech = api.GetSearch(
    raw_query="l=en&q=Giveaway%20logitech%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Logitech'] = search_logitech
search_nvidia = api.GetSearch(
    raw_query="l=en&q=Giveaway%20Nvidia%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Nvidia'] = search_nvidia
search_hashtag_giveaway = api.GetSearch(
    raw_query="l=en&q=%23Giveaway%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['#Giveaway'] = search_hashtag_giveaway
search_itunes = api.GetSearch(
    raw_query="l=en&q=Giveaway%20Itunes%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Itunes'] = search_itunes
search_googleplay = api.GetSearch(
    raw_query="l=en&q=Giveaway%20google%20play%20since%3A" + today.year + "-" + today.month + "-" + today.day + "%20until%3A" + future_date.year + "-" + future_date.month + "-" + future_date.day + "&src=typd&count=100")
results['Google Play'] = search_googleplay

# Enter all tweets found in search above
for tweet in results['default']:
    try:
        enter_giveaway(api, tweet)
    except twitter.TwitterError:
        pass
