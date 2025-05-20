import os, json
from package.livro import Livro
from package.database import Database
from package.utils import Utils

class Biblioteca():
    def __init__(self, qtd=1):
        self.quantidade = int(qtd)
        self.db = Database()
        self.u = Utils()
        
    def adicionar_livro(self, titulo, autor, ano, ISBN):
        livro = Livro(titulo, autor, ano, ISBN).gerar_livro()
        livros = self.db.abrir_data("biblioteca")
        
        if livro["titulo"] == None or livro["autor"] == None or livro["ano"] == None or livro["ISBN"] == None:
            print("Erro ao adicionar livro")
            return False
        
        for l in livros:
            if livro["ISBN"] == l["ISBN"]:
                print("Livro já cadastrado na biblioteca")
                return False
                
        livro["quantidade"] = self.quantidade
        print("Livro cadastrado na biblioteca com sucesso.")
                
        livros.append(livro)
        
        self.db.salvar_data("biblioteca", livros)
        self.u.atualizar_estoque()
        return True

