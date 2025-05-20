import os, json
from package.database import Database
from package.cripto import Criptografia
    
class User(Criptografia):
    def __init__(self, first_name, last_name, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.password = Criptografia().criptografar(password)
        self.email = email
        self.db = Database()
        
    def gerar_cadastro(self):
        self.cadastro = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "email": self.email,
        } 
        
        return self.cadastro
     
class Funcionario(User):
    def __init__(self, first_name, last_name, password, email):
        super().__init__(first_name, last_name, password, email)
        self.admin = False
        self.funcionario = True
        
    def gerar_codigo_funcionario(self):
        usuarios = self.db.abrir_data("user")
        if len(usuarios) > 0:
            for usuario in usuarios[::-1]:
                if usuario["admin"] == False and usuario["funcionario"] == True:
                    ultimo_codigo = int(usuario["codigo"][1:])
                    self.codigo = "F" + str(ultimo_codigo + 1)
                    break
                    
                else:
                    self.codigo = "F1"
        else:
            self.codigo = "F1"
            
    def promover_conta_cliente(self):
        usuarios = self.db.abrir_data("users")
            
        for conta in usuarios:
            if conta["email"] == self.email:
                usuarios.remove(conta)
                break
        
        self.db.salvar_data("users", usuarios)
        self.gerar_cadastro()
            
    def gerar_cadastro(self):
        self.cadastro = super().gerar_cadastro()
        self.gerar_codigo_funcionario()
        self.cadastro["codigo"] = self.codigo
        self.cadastro["funcionario"] = self.funcionario
        self.cadastro["admin"] = self.admin
        
        self.db.salvar_cadastro(self.cadastro)
        
class Cliente(User):
    def __init__(self, first_name, last_name, password, email):
        super().__init__(first_name, last_name, password, email)
        self.admin = False
        self.funcionario = False
    
    def is_admin(self):
        return False
            
    def gerar_codigo_cliente(self):
        usuarios = self.db.abrir_data("users")     
        if len(usuarios) > 0:
            for usuario in usuarios[::-1]:
                if usuario["admin"] == False and usuario["funcionario"] == False:
                    ultimo_codigo = int(usuario["codigo"][1:])
                    self.codigo = "C" + str(ultimo_codigo + 1)
                    break
                
                else:
                    self.codigo = "C1"
            
        else:
            self.codigo = "C1"
            
    def gerar_cadastro(self):
        self.cadastro = super().gerar_cadastro()
        self.gerar_codigo_cliente()
        self.cadastro["codigo"] = self.codigo
        self.cadastro["funcionario"] = self.funcionario
        self.cadastro["admin"] = self.admin
        
        self.db.salvar_cadastro(self.cadastro)
            
class Admin(User):
    def __init__(self, first_name, last_name, password, email):
        super().__init__(first_name, last_name, password, email)
        self.admin = True
        self.funcionario = True
        
    def gerar_codigo_admin(self):
        usuarios = self.db.abrir_data("users")
                
        if len(usuarios) > 0:
            for usuario in usuarios[::-1]:
                if usuario["admin"] == True and usuario["funcionario"] == True:
                    ultimo_codigo = int(usuario["codigo"][1:])
                    self.codigo = "A" + str(ultimo_codigo + 1)
                    break
                
                else:
                    self.codigo = "A1"
            
        else:
            self.codigo = "A1"
            
    def gerar_cadastro(self):
        self.cadastro = super().gerar_cadastro()
        self.gerar_codigo_admin()
        self.cadastro["codigo"] = self.codigo
        self.cadastro["funcionario"] = self.funcionario
        self.cadastro["admin"] = self.admin
        
        self.db.salvar_cadastro()

# logica pra ler o json e pegar os atributos
# instanciar um objeto temporario com os atributos temp = User(a1, a2, a3, a4)
# temp.trocar_senha()