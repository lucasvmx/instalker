#
# Software para verificar se um determinado usuário curtiu uma foto específica
# Autor: Lucas Vieira de Jesus <lucas.engen.cc@gmail.com>
# Funciona com contas públicas e privadas (desde que você siga a conta privada)

import instaloader
from sys import exit, argv
import dotenv
from os import getenv
from user_like import user_liked
from snapshot import do_snapshot
from login import perform_login
from credentials import Credentials
from bot import setup_bot, send_message

valid_timeout_strings = ["2h", "4h", "6h", "12h", "24h"]

# nome do recurso (parte da URL)
resource=''

# nome do usuário a ser verificado
username=''

def show_usage():
    """Exibe instruções de uso do programa
    e depois finaliza-o
    """
    
    usage_str = '''Usage: python {} <username> <resource> or
python {} --snapshot <timeout>

<resource>: name of resource to be searched
<username>: name of user to check for likes
--snapshot: run program in snapshot mode (unfollowers finder)
<timeout>: can be 2h, 4h, 6h, 12h or 24h
    '''
    
    print("[ERROR] Wrong number of arguments: {}\n".format(len(argv)))
    print(usage_str.format(argv[0], argv[0]))
    exit(1)

if __name__ == "__main__":
    snapshot_mode = False
    skip_login = False
    timeout_string = ''

    if len(argv) == 3 and argv[1] == "--snapshot":
        snapshot_mode = True
        timeout_string = argv[2]
        if not timeout_string in valid_timeout_strings:
            print("[ERROR] INVALID TIMEOUT STRING SPECIFIED")
            show_usage()
    elif len(argv) != 3:
        show_usage()

    # Carrega as variáveis de ambiente
    if dotenv.find_dotenv() == "":
        print("[ERROR] Failed to load .env")
        exit(1)


    dotenv.load_dotenv()

    # configura o BOT do telegram
    setup_bot()
    send_message("Instalker starting :)")

    try:
        if getenv("SERVER_IP") is None:
            raise Exception("wrong type")

        size = len(getenv("SERVER_IP"))
        if size == 0:
            raise Exception("wrong length")
    except Exception as e:
        print("[ERROR] Invalid SERVER_IP setting: {}".format(e))
        exit(1)

    # Obtém e valida as credenciais fornecidas
    creds = Credentials()
    if not creds.validate():
        print("[ERROR] Invalid credentials")
        exit(1)

    # Cria a instância global
    instance = instaloader.Instaloader()

    try:
        instance.load_session_from_file(creds.get_user())
        skip_login = True
    except FileNotFoundError:
        print("[WARNING] Session not found")

    # Realiza o login
    try:
        perform_login(instance, creds, skip_login)
    except Exception as err:
        print("[ERROR] Could not login: {}".format(err))
        exit(1)

    if snapshot_mode == True:
        do_snapshot(instance, creds.get_user(), timeout_str=timeout_string)
    else:
        # Realiza a tarefa de verificar se um usuário curtiu o post
        user_liked(instance)
