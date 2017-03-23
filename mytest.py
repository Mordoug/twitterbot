import twitter 
from datetime import *

def enter_giveaway(api, status):
    '''
    Pre: Pass in an API object and a twitter.Status object
    Post: Retweet the tweet, favorite the tweet, and/or follow the user who posted the tweet as necessary
    Purpose: Enter a twitter giveaway based on instructions in the tweet
    '''
    RT = False # Track if retweeting is necessary
    
    # Convert the twitter.Status object into a string and split it up to enable use of the status id and screen name
    status_string = status.__repr__()
    attributes = status_string.split(',')
    status_id = attributes[0].split('=')
    screen_name = attributes[1].split('=')
    
    # Convert the twitter.Status string from unicode to ascii
    status_str = status_string.encode('ascii', 'ignore')
    status_str = status_str.lower()
    
    # Check and act upon entry requirements of the giveaway
    if ' rt ' in status_str:
        RT = True
    if ' rt' in status_str:
        RT = True
    if 'retweet' in status_str:
        RT = True
        
    if RT == True:
        api.PostRetweet(status_id[1])
    if 'follow' in status_str:
        api.CreateFriendship(None, screen_name[1])
    if 'favorite' in status_str:
        api.CreateFavorite(None, status_id[1])
        

# Create an API object to interact with the Twitter API
api = twitter.Api(
    consumer_key = 'JkLa7tiZDkRkEHAVs9rRs8q5z',
    consumer_secret = '5uNENyyQVLsJxANWBG57gWVjfIWwTxuRKMMEvpbHds754rqWjS',
    access_token_key = '3442532363-awZtxIgpTv3dpXUbjyb0NXjTk8YWYdvcljZigor',
    access_token_secret = 't005Jq27nOqXfTQcE7AYfy5Y0q6ASQ9xYqU1mUsQdRrQb'
)
      
#print(api.VerifyCredentials())

# Get 100 twitter.Status objects (tweets) containing the word "Giveaway"
results = api.GetSearch(
    raw_query="l=en&q=Giveaway%20since%3A2017-03-20%20until%3A2017-03-21&src=typd&count=100")  

#print ("%s", (results))

# Enter all tweets found in search above
for tweet in results:
    try:
        enter_giveaway(api, tweet)
    except (twitter.TwitterError):
        pass
        