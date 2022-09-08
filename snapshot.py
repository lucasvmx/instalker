from credentials import Credentials
import instaloader
from time import sleep
from sys import exit
from signal import signal, SIGTERM, SIGINT
from threading import Lock

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

def do_snapshot(instance: instaloader.Instaloader, profile_name: str):

    global should_exit
    should_exit = False
    
    print("[INFO] Setting up signal handlers ...")
    signal(SIGTERM, handle_cleanup)
    signal(SIGINT, handle_cleanup)

    while True:

        # Verifica se o programa deve ser fechado
        mux.acquire()
        if should_exit:
            mux.release()
            break
            
        mux.release()

        # Obtém a lista de seguidores a cada 12 horas
        old_followers = get_followers(instance, profile_name)
        sleep(43200)
        current_followers = get_followers(instance, profile_name)
        sleep(43200)
        excluded = compare_list(old_followers, current_followers)
        if len(current_followers) < len(old_followers):
            for follower in excluded:
                print("[INFO] {} unfollowed you".format(follower))
        else:
            print("[INFO] Followers checking completed! Current followers: {}".format(len(current_followers)))
