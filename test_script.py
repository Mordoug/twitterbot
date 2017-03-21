from python-twitter import *
from datetime import *

    api = Twitter.Api(
        consumer_key = 'JkLa7tiZDkRkEHAVs9rRs8q5z',
        consumer_secret = '5uNENyyQVLsJxANWBG57gWVjfIWwTxuRKMMEvpbHds754rqWjS',
        access_token = '3442532363-awZtxIgpTv3dpXUbjyb0NXjTk8YWYdvcljZigor',
        access_token_secret = 't005Jq27nOqXfTQcE7AYfy5Y0q6ASQ9xYqU1mUsQdRrQb'
    )
      
    print(api.VerifyCredentials())

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['Giveaway']) # let's define all words we would like to have a look for
        tso.set_language('en') #ony want to see english tweets
        #tso.set_until(date) #we  only want to see current giveaways, dont 
        tso.set_include_entities(False) # and don't give us all those entity information

        

