class Livro():
    def __init__(self, titulo, autor, ano, ISBN):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.ISBN = ISBN
        
    def gerar_livro(self):
        livro = {
            "titulo" : self.titulo,
            "autor" : self.autor,
            "ano" : self.ano,
            "ISBN" : self.ISBN,
            "quantidade" : 0,
            "disponivel" : False
        }
        
        return livro