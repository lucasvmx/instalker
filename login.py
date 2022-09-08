import instaloader
from credentials import Credentials
import sys
from threading import Lock, Thread
from time import sleep
from server import start_http_server
from two_factor_code import get_two_factor_code

def perform_login(loader_instance: instaloader.Instaloader, creds: Credentials, skip_login: bool):
    if skip_login == False:
        try:
            print("[INFO] Logging in ...")
            loader_instance.login(creds.get_user(), creds.get_passwd())
        except instaloader.exceptions.TwoFactorAuthRequiredException as err:

            start_http_server()

            print("[WARNING] Two factor code required. Go to http://192.168.1.2:3333 and insert it")
            print("[INFO] Waiting for two factor code ...")

            while len(get_two_factor_code()) == 0:
                sleep(1)

            server_thread._stop()

            print("[INFO] Code: {}".format(two_factor_code.strip()))

            # Tenta realizar o login utilizando o código de autenticação em dois fatores
            try:
                loader_instance.two_factor_login(two_factor_code.strip())
            except instaloader.exceptions.BadCredentialsException as fail:
                print("[ERROR] Invalid credentials provided")
                sys.exit(1)
        
        
        # Salva a sessão
        loader_instance.save_session_to_file()

