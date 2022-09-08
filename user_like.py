import sys
from os import getenv
import instaloader
from login import perform_login
from credentials import Credentials

def parse_args():
    username = ""
    resource = ""

    # Analisa os argumentos
    for arg in sys.argv:
        if arg == sys.argv[0]:
            continue

        if resource == "":
            resource = arg
        elif username == "":
            username = arg
        else:
            print("[WARNING] Ignoring {}".format(arg))
    
    return {
        "username": username,
        "resource": resource
    }

def user_liked(loader_instance: instaloader.Instaloader):

    data = parse_args()
    username = data["username"]
    resource = data["resource"]

    print("[INFO] Finding out if user '{}' liked '{}' ...".format(username, resource))
    Post = instaloader.Post.from_shortcode(loader_instance.context, resource)

    try:
        # Obtém as curtidas do post
        global likes
        
        owner = Post.owner_username

        print("[INFO] Checking if {} liked the post from {}".format(username, owner))

        likes = Post.get_likes()

        # Lista as curtidas
        for like in likes:
            if like.username == username:
                print("[INFO] {} liked the post :)".format(username))
                sys.exit(0)

        print("[INFO] {} didn't liked the post :(".format(username))
    except instaloader.exceptions.LoginRequiredException as err:
        print("[ERROR] Can't get likes: {}".format(err))
    except instaloader.exceptions.BadResponseException as err:
        print("[ERROR] Bad response received: {}".format(err))
        print("Is the resource URL valid?")