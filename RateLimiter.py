from Queue import *
from enum import Enum
import threading


class RateLimiter:
    def __init__(self, auth_type):
        self.auth_type = auth_type.value
        self.monitored_rate_limits = {}

        self.API_WINDOW = 15  # seconds

    def execute_allowed_api_calls(self, rate_limit):
        api_queue = self.monitored_rate_limits[rate_limit.name]["api_queue"]
        limits = list(self.monitored_rate_limits[rate_limit.name]["value"])
        limit = limits[self.auth_type]
        while limit > 0:
            if api_queue.empty():
                break

            next_call = api_queue.get()
            print("executing api call: " + str(next_call))

            next_call[0](*next_call[1])
            limit -= 1
            limits[self.auth_type] = limit
            self.monitored_rate_limits[rate_limit.name]["value"] = tuple(limits)

    def timer_callback(self, rate_limit, api_call, *parameters):
        self.monitored_rate_limits[rate_limit.name]["value"] = rate_limit.value
        self.execute_allowed_api_calls(rate_limit)
        threading.Timer(self.API_WINDOW, self.timer_callback, [rate_limit, api_call, parameters]).start()

    def remove_rate_limit(self, rate_limit):  # TODO
        pass

    def add_api_call(self, rate_limit, api_call, *parameters):
        if rate_limit.name not in self.monitored_rate_limits:
            print("new rate limit added: " + rate_limit.name)
            self.monitored_rate_limits[rate_limit.name] = {
                "value": rate_limit.value,
                "api_queue": Queue()
            }
            threading.Timer(self.API_WINDOW, self.timer_callback, [rate_limit, api_call, parameters]).start()

        self.monitored_rate_limits[rate_limit.name]["api_queue"].put((api_call, parameters))
        self.execute_allowed_api_calls(rate_limit)


class TwitterAuthType(Enum):
    USER_AUTH = 0
    APP_AUTH = 1


class TwitterRateLimit(Enum):
    # https://dev.twitter.com/rest/public/rate-limits
    ACCOUNT_VERIFY_CREDENTIALS = (75, 0)
    APPLICATION_RATE_LIMIT_STATUS = (180, 180)
    FAVORITES_LIST = (75, 75)
    FOLLOWERS_IDS = (15, 15)
    FOLLOWERS_LIST = (15, 15)
    FRIENDS_IDS = (15, 15)
    FRIENDS_LIST = (15, 15)
    FRIENDSHIPS_SHOW = (180, 15)
    GEO_ID = (75, 0)
    HELP_CONFIGURATION = (15, 15)
    HELP_LANGUAGES = (15, 15)
    HELP_PRIVACY = (15, 15)
    HELP_TOS = (15, 15)
    LISTS_LIST = (15, 15)
    LISTS_MEMBERS = (900, 75)
    LISTS_MEMBERS_SHOW = (15, 15)
    LISTS_MEMBERSHIPS = (75, 75)
    LISTS_OWNERSHIPS = (15, 15)
    LISTS_SHOW = (75, 75)
    LISTS_STATUSES = (900, 900)
    LISTS_SUBSCRIBERS = (180, 15)
    LISTS_SUBSCRIBERS_SHOW = (15, 15)
    LISTS_SUBSCRIPTIONS = (15, 15)
    SEARCH_TWEETS = (180, 450)
    STATUSES_LOOKUP = (900, 300)
    STATUSES_MENTIONS_TIMELINE = (75, 0)
    STATUSES_RETWEETERS_IDS = (75, 300)
    STATUSES_RETWEETS_OF_ME = (75, 0)
    STATUSES_RETWEETS = (75, 300)
    STATUSES_SHOW = (900, 900)
    STATUSES_USER_TIMELINE = (900, 1500)
    TRENDS_AVAILABLE = (75, 75)
    TRENDS_CLOSEST = (75, 75)
    TRENDS_PLACE = (75, 75)
    USERS_LOOKUP = (900, 300)
    USERS_SEARCH = (900, 0)
    USERS_SHOW = (900, 900)
    USERS_SUGGESTIONS = (15, 15)
    USERS_SUGGESTIONS_SLUG = (15, 15)
    USERS_SUGGESTIONS_SLUG_MEMBERS = (15, 15)
