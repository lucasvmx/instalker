import instaloader
from credentials import Credentials
from sys import exit
from time import sleep
from server import start_http_server
from two_factor_code import get_two_factor_code
from multiprocessing import Process
from bot import send_message
from logging import error, info, warn

def mask_2fa_code(code: str) -> str:
    masked = ""
    sz = len(code)
    if sz != 6:
        return "*" * 6 

    for i in range(sz):
        if i < 4:
            masked += "*"
        else:
            masked += code[i]
    
    return masked

def perform_login(loader_instance: instaloader.Instaloader, creds: Credentials, skip_login: bool):
    if skip_login == False:
        try:
            info("logging in ...")
            loader_instance.login(creds.get_user(), creds.get_passwd())
        except instaloader.exceptions.TwoFactorAuthRequiredException as err:
            send_message("Insert your two factor auth code")
            warn("two factor code required. Go to http://192.168.1.2:3333 and insert it")
            info("waiting for two factor code ...")

            try:
                p = Process(target=start_http_server)
                p.start()

            except Exception as err:
                error("failed to start HTTP server: {}".format(err))
                exit(1)

            two_factor_code = ''

            info("polling for 2FA code")
            while True:
                two_factor_code = get_two_factor_code()
                if len(two_factor_code) > 0:
                    break
                sleep(1)

            info("code received from server: {}".format(mask_2fa_code(two_factor_code.strip())))

            # Tenta realizar o login utilizando o código de autenticação em dois fatores
            try:
                loader_instance.two_factor_login(two_factor_code.strip())
            except instaloader.exceptions.BadCredentialsException as fail:
                error("invalid credentials provided")
                exit(1)
        
        
        info("login successful")

        # Salva a sessão
        loader_instance.save_session_to_file()
