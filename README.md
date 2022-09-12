# Instalker

Ferramenta simples criada para verificar se um usuário curtiu um determinado post ou se alguém deixou de te seguir. Suporta a autenticação de dois
fatores

# Instalação

```bash
pip install -r requirements.txt
```

# Uso

## Modo profile checker
Esse modo verifica se um usuário curtiu um certo post

1 - Crie o arquivo de configurações e insira as credenciais da sua conta:

```bash
touch .env
echo "USERNAME=mylogin" > .env
echo "PASSWORD=mypassword" >> .env
```

2 - Execute o programa

```bash
python main.py ChpewYuhfg4 instagram
```

O comando acima irá verificar se o usuário `instagram` curtiu o post com ID `ChpewYuhfg4`

A URL pode ser obtida ao clicar no post. Veja o exemplo a seguir:

* `https://www.instagram.com/p/`<**POST ID**>



```bash
python main.py --snapshot <timeout>
```

## Modo snapshot

O modo snapshot cria um serviço que te avisa por telegram/console quem deixou de te seguir.
Para utilizar esse modo, utilize o bot father para criar um bot do telegram e obter um token.

### Para usar o bot do telegram:
* Crie um bot no telegram [BotFather](https://t.me/botfather)
* Obtenha o token
* Crie um grupo (ou channel) e insira o bot nele
* Obtenha o ID do channel (ou grupo)

1 - Crie as configurações

```bash
echo "USERNAME=mylogin" > .env
echo "PASSWORD=mypassword" >> .env
echo "SERVER_IP=0.0.0.0" >> .env
echo "TOKEN=mytelegrambottoken" >> .env
echo "CHAT_ID=mytelegramchatid" >> .env
```

3 - Instale o serviço
```bash
sudo su
./install.sh
```

Se o serviço for configurado corretamente, você receberá uma mensagem no telegram avisando que o programa foi carregado

