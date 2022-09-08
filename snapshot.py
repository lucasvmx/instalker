from credentials import Credentials
import instaloader
from time import sleep
from sys import exit
from signal import signal, SIGTERM, SIGINT
from threading import Lock
from bot import send_message

def get_followers(instance: instaloader.Instaloader, profile_name: str):

    print("[INFO] Getting followers of {}".format(profile_name))

    try:
        global profile 
        profile = instaloader.Profile.from_username(instance.context, username=profile_name)
    except instaloader.ProfileNotExistsException as e:
        print("[ERROR] The profile {} does not exists".format(profile_name))
        exit(1)

    followers_list = set(profile.get_followers())

    followers = [""]

    for follower in followers_list:
        followers.append(follower.username)

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


def handle_cleanup(signum, frame):
    print("[INFO] Cleaning up ...")
    mux.acquire()
    should_exit = True
    mux.release()
    exit(0)

def setup_snapshot():
    global mux
    mux = Lock()

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

    global should_exit
    should_exit = False
    timeout = calculate_time(timeout_string=timeout_str)
    
    print("[INFO] Setting up signal handlers ...")
    signal(SIGTERM, handle_cleanup)
    signal(SIGINT, handle_cleanup)

    send_message("Capturando snapshot de seguidores a cada {}".format(timeout_str))

    while True:

        # Verifica se o programa deve ser fechado
        mux.acquire()
        if should_exit:
            mux.release()
            break
            
        mux.release()

        # Obtém a lista de seguidores a cada X horas
        old_followers = get_followers(instance, profile_name)
        sleep(timeout)
        current_followers = get_followers(instance, profile_name)
        sleep(timeout)
        excluded = compare_list(old_followers, current_followers)
        if len(current_followers) < len(old_followers):
            for follower in excluded:
                print("[INFO] {} unfollowed you".format(follower))
                send_message("{} deixou de te seguir".format(follower))
        else:
            print("[INFO] Followers checking completed! Current followers: {}".format(len(current_followers)))
