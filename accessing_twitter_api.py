import twitter
import time

print("1. Create your application info here: https://apps.twitter.com")
print("When you have created the application, enter:")
app_name = input("Enter your application name: ")
consumer_key = input("Enter your consumer key: ")
consumer_secret = input("Enter your consumer secret: ")

print("2. Now, authorize this application.")
print("It sends the user to the authorize page - accept authorize page.")
time.sleep(3)

access_key, access_secret = twitter.oauth_dance(app_name, consumer_key, consumer_secret)
print("Finihed.")
print("---------Copy and past the information below into config.py----------:")
print("consumer_key = '%s'" % consumer_key)
print("consumer_secret = '%s'" % consumer_secret)
print("access_key = '%s'" % access_key)
print("access_secret = '%s'" % access_secret)