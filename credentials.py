#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import getenv

class Credentials:

    # Dicionário que armazena as credenciais
    credentials = {
        "username": "", 
        "password": ""
    }

    def __init__(self):
        """Cria uma instância da classe a partir das variáveis de ambiente
        """
        self.credentials["username"] = getenv("USERNAME")
        self.credentials["password"] = getenv("PASSWORD")
        

    def get_user(self) -> str:
        return self.credentials["username"]
    
    def get_passwd(self) -> str:
        return self.credentials["password"]
    
    def set_user(self, user: str):
        self.credentials["username"] = user
    
    def set_passwd(self, passwd: str):
        self.credentials["password"] = passwd

    def validate(self) -> bool:
        return len(self.credentials["username"]) > 0 and len(self.credentials["password"]) > 0
