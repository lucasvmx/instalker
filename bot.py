from os import getenv
from requests import get
from urllib import parse
from sys import exit

def setup_bot():
    global baseURL, CHAT_ID, TOKEN

    baseURL = "https://api.telegram.org/"
    CHAT_ID = getenv("CHAT_ID")
    TOKEN = getenv("TOKEN")

    try:
        len(CHAT_ID)
        len(TOKEN)
    except:
        print("[ERROR] Please setup CHAT_ID and TOKEN")
        exit(1)

def buildURL(token: str, chatId: str, msg: str) -> str: 
	s = baseURL
	s += "bot{}/sendMessage?".format(parse.quote(token))
	s += "chat_id={}".format(parse.quote(chatId))
	s += "&text={}".format(parse.quote(msg))
	return s

def send_message(msg: str):
    full_msg = "[INSTALKER] {}".format(msg)
    response_obj = get(url=buildURL(TOKEN, CHAT_ID, full_msg))
    print("[INFO] Request status: {}".format(response_obj.status_code))
