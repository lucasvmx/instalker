#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv, exit
from instaloader import Instaloader, Post
from instaloader.exceptions import LoginRequiredException, BadResponseException
from logging import warn, info, error

def parse_args():
    username = ""
    resource = ""

    # Analisa os argumentos
    for arg in argv:
        if arg == argv[0]:
            continue

        if resource == "":
            resource = arg
        elif username == "":
            username = arg
        else:
            warn("Ignoring {}".format(arg))
    
    return {
        "username": username,
        "resource": resource
    }

def user_liked(loader_instance: Instaloader):

    data = parse_args()
    username = data["username"]
    resource = data["resource"]

    info("finding out if user '{}' liked '{}' ...".format(username, resource))
    post = Post.from_shortcode(loader_instance.context, resource)

    try:
        # Obtém as curtidas do post
        global likes
        
        owner = post.owner_username

        info("checking if {} liked the post from {}".format(username, owner))

        likes = post.get_likes()

        # Lista as curtidas
        for like in likes:
            if like.username == username:
                info("{} liked the post :)".format(username))
                exit(0)

        info("{} didn't liked the post :(".format(username))
    except LoginRequiredException as err:
        error("can't get likes: {}".format(err))
    except BadResponseException as err:
        error("bad response received: {}".format(err))
        error("is the resource URL valid?")
