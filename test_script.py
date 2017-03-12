from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Giveaway']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'JkLa7tiZDkRkEHAVs9rRs8q5z',
        consumer_secret = '5uNENyyQVLsJxANWBG57gWVjfIWwTxuRKMMEvpbHds754rqWjS',
        access_token = '3442532363-awZtxIgpTv3dpXUbjyb0NXjTk8YWYdvcljZigor',
        access_token_secret = 't005Jq27nOqXfTQcE7AYfy5Y0q6ASQ9xYqU1mUsQdRrQb'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
    
