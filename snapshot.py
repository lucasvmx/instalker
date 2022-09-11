import instaloader
from time import sleep
from sys import exit
from bot import send_message
from logging import info, error

def get_followers(instance: instaloader.Instaloader, profile_name: str):

    info("getting followers of {}".format(profile_name))

    try:
        global profile 
        profile = instaloader.Profile.from_username(instance.context, username=profile_name)
        info("loaded profile {}".format(profile_name))
    except instaloader.ProfileNotExistsException as e:
        error("the profile {} does not exists".format(profile_name))
        exit(1)
    except instaloader.QueryReturnedBadRequestException as e:
        error("could not load profile: {}".format(e))
        return [""]

    try:
        f = profile.get_followers()
    except Exception as err:
        error("could not get followers list: {}".format(err))
        return [""]

    followers_list = set(f)

    followers = [""]

    for follower in followers_list:
        followers.append(follower.username)

    info("fetched {} followers from {}".format(len(followers), profile_name))
    return followers

def compare_list(list1=[],list2=[]):
    
    excluded = set([])

    # Busca os itens da lista 1 na lista 2
    for item1 in list1:
        if not item1 in list2:
            excluded.add(item1)

    # Busca os itens da lista 2 na lista 1
    for item1 in list2:
        if not item1 in list1:
            excluded.add(item1)
    
    return excluded

def calculate_time(timeout_string: str) -> int:
    valid_timeout_strings = {
        "2h": 3600, 
        "4h": 14400, 
        "6h": 21600, 
        "12h": 43200, 
        "24h": 86400
    }

    if not timeout_string in valid_timeout_strings.keys():
        return 0

    return valid_timeout_strings[timeout_string]

def do_snapshot(instance: instaloader.Instaloader, profile_name: str, timeout_str: str):

    timeout = calculate_time(timeout_string=timeout_str)

    send_message("Capturando snapshot de seguidores a cada {}".format(timeout_str))

    while True:

        # Obtém a lista de seguidores a cada X horas
        while True:
            old_followers = get_followers(instance, profile_name)
            if len(old_followers) == 0:
                error("failed to get followers list #1")
                sleep(300)
                continue
            break

        sleep(timeout)
        while True:
            current_followers = get_followers(instance, profile_name)
            if len(current_followers) == 0:
                error("failed to get followers list #2")
                sleep(300)
                continue
            break

        info("followers checking completed! Current followers: {}".format(len(current_followers)))

        excluded = compare_list(old_followers, current_followers)
        if len(excluded) > 0:
            for follower in excluded:
                info("{} unfollowed you".format(follower))
                send_message("{} deixou de te seguir".format(follower))
        
        sleep(timeout)
            
