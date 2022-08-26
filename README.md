# Instalker

Ferramenta simples criada para verificar se um usuário curtiu um determinado post. Suporta a autenticação de dois
fatores

# Instalação

```bash
pip install -r requirements.txt
```

# Uso

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
