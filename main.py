#
# Software para verificar se um determinado usuário curtiu uma foto específica
# Autor: Lucas Vieira de Jesus <lucas.engen.cc@gmail.com>
# Funciona apenas com as fotos públicas

import instaloader
import sys
import dotenv
from os import getenv

# nome do recurso (parte da URL)
resource=''

# nome do usuário a ser verificado
username=''

# Dicionário que armazena as credenciais
credentials = {
    "username": "", 
    "password": ""
}

def validate_credentials():
    return len(credentials["username"]) > 0 and len(credentials["password"]) > 0

def show_usage():
    """Exibe instruções de uso do programa
    e depois finaliza-o
    """
    
    usage_str = '''Usage: python {} <resource> <username>

<resource>: name of resource to be searched
<username>: name of user to check for likes
    '''
    
    print("[ERROR] Wrong number of arguments: {}\n".format(len(sys.argv)))
    print(usage_str.format(sys.argv[0]))
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        show_usage()

    # Carrega as variáveis de ambiente
    if dotenv.find_dotenv() == "":
        print("[ERROR] Failed to load .env")
        sys.exit(1)

    dotenv.load_dotenv()

    uname = getenv("USERNAME")
    psw = getenv("PASSWORD")
    if uname != None:
        credentials["username"] = uname
    if psw != None:
        credentials["password"] = psw

    if not validate_credentials():
        print("[ERROR] Empty username or password")
        sys.exit(1)

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

    loader_instance = instaloader.Instaloader()

    # flag para determinar se o login precisa ser feito
    skip_login = False

    try:
        loader_instance.load_session_from_file(credentials["username"])
        skip_login = True
    except FileNotFoundError:
        print("[WARNING] Session not found")
    
    # Realiza o login
    if skip_login == False:
        try:
            print("[INFO] Logging in ...")
            loader_instance.login(credentials["username"], credentials["password"])
        except instaloader.exceptions.TwoFactorAuthRequiredException as err:
            two_factor_code = input("[WARNING] Two factor code required. Insert it here: ")
            print("[INFO] Code: {}".format(two_factor_code.strip()))

            # Tenta realizar o login utilizando o código de autenticação em dois fatores
            try:
                loader_instance.two_factor_login(two_factor_code.strip())
            except instaloader.exceptions.BadCredentialsException as fail:
                print("[ERROR] Invalid credentials provided")
                sys.exit(1)
        
        # Salva a sessão
        loader_instance.save_session_to_file()

    print("[INFO] Finding out if user '{}' liked '{}' ...".format(username, resource))
    Post = instaloader.Post.from_shortcode(loader_instance.context, resource)

    try:
        # Obtém as curtidas do post
        global likes
        
        likes = Post.get_likes()
        # Lista as curtidas
        for like in likes:
            if like.username == username:
                print("[INFO] {} liked the post :)".format(username))
                sys.exit(0)

        print("[INFO] {} didn't liked the post :(".format(username))
    except instaloader.exceptions.LoginRequiredException as err:
        print("[ERROR] Can't get likes: {}".format(err))
