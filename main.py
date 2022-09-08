#
# Software para verificar se um determinado usuário curtiu uma foto específica
# Autor: Lucas Vieira de Jesus <lucas.engen.cc@gmail.com>
# Funciona com contas públicas e privadas (desde que você siga a conta privada)

import instaloader
import sys
import dotenv
from os import getenv
from user_like import user_liked
from snapshot import do_snapshot, setup_snapshot
from login import perform_login
from credentials import Credentials
from threading import Lock

# nome do recurso (parte da URL)
resource=''

# nome do usuário a ser verificado
username=''

def show_usage():
    """Exibe instruções de uso do programa
    e depois finaliza-o
    """
    
    usage_str = '''Usage: python {} <username> <resource> or
python {} --snapshot

<resource>: name of resource to be searched
<username>: name of user to check for likes
--snapshot: run program in snapshot mode (unfollowers finder)
    '''
    
    print("[ERROR] Wrong number of arguments: {}\n".format(len(sys.argv)))
    print(usage_str.format(sys.argv[0], sys.argv[0]))
    sys.exit(1)

if __name__ == "__main__":
    snapshot_mode = False
    skip_login = False

    if len(sys.argv) == 2 and sys.argv[1] == "--snapshot":
        snapshot_mode = True
    elif len(sys.argv) != 3:
        show_usage()

    # Carrega as variáveis de ambiente
    if dotenv.find_dotenv() == "":
        print("[ERROR] Failed to load .env")
        sys.exit(1)

    dotenv.load_dotenv()

    try:
        if getenv("SERVER_IP") is None:
            raise Exception("wrong type")

        size = len(getenv("SERVER_IP"))
        if size == 0:
            raise Exception("wrong length")
    except Exception as e:
        print("[ERROR] Invalid SERVER_IP setting: {}".format(e))
        sys.exit(1)

    # Obtém e valida as credenciais fornecidas
    creds = Credentials()
    if not creds.validate():
        print("[ERROR] Invalid credentials")
        sys.exit(1)

    # Cria a instância global
    instance = instaloader.Instaloader()

    try:
        instance.load_session_from_file(creds.get_user())
        skip_login = True
    except FileNotFoundError:
        print("[WARNING] Session not found")

    # Realiza o login
    perform_login(instance, creds, skip_login)
    
    if snapshot_mode == True:
        setup_snapshot()
        do_snapshot(instance, creds.get_user())
    else:
        # Realiza a tarefa de verificar se um usuário curtiu o post
        user_liked(instance)
