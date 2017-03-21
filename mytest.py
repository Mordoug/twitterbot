import twitter 
from datetime import *

api = twitter.Api(
    consumer_key = 'JkLa7tiZDkRkEHAVs9rRs8q5z',
    consumer_secret = '5uNENyyQVLsJxANWBG57gWVjfIWwTxuRKMMEvpbHds754rqWjS',
    access_token_key = '3442532363-awZtxIgpTv3dpXUbjyb0NXjTk8YWYdvcljZigor',
    access_token_secret = 't005Jq27nOqXfTQcE7AYfy5Y0q6ASQ9xYqU1mUsQdRrQb'
)
      
#print(api.VerifyCredentials())


results = api.GetSearch(
    raw_query="l=en&q=Giveaway%20since%3A2017-03-20%20until%3A2017-03-21&src=typd&count=100")  

print ("%s", (results))