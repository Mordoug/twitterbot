import twitter

def enter_giveaway(api, status_id, RT, follow, favorite):    
    if RT == True:
        api.PostRetweet(status_id)
    if follow == True:
        status = api.GetStatus(status_id)
        status_string = status.__repr__()
        attributes = status_string.split(',')
        screen_name = attributes[1].split('=')
        api.CreateFriendship(None, screen_name[1])
    if favorite == True:
        api.CreateFavorite(None, status_id)
        