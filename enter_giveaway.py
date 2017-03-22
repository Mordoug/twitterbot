import twitter

def enter_giveaway(api, status): 
    RT = False

    status_string = status.__repr__()
    attributes = status_string.split(',')
    status_id = attributes[0].split('=')
    screen_name = attributes[1].split('=')
    
    status_str = status_string.encode('ascii', 'ignore')
    str.lower(status_str)
    
    if 'rt' in status_str:
        RT = True
    if 'retweet' in status_str:
        RT = True
        
    if RT == True:
        api.PostRetweet(status_id[1])
    if 'follow' in status_str:
        api.CreateFriendship(None, screen_name[1])
    if 'favorite' in status_str:
        api.CreateFavorite(None, status_id[1])