class Criptografia:
        def __init__ (self, chave=3):
            self.chave = chave
        def criptografar (self, senha):
            senha_cripto = ""
            
            for c in senha:
                num_char = ord(c)
                novo_char = chr(num_char + self.chave)
                senha_cripto += novo_char
                
            return senha_cripto
        
        def descriptografar (self, senha_cripto):
            senha = ""
            
            for c in senha_cripto:
                num_char = ord(c)
                novo_char = chr(num_char - self.chave)
                senha += novo_char
                
            return senha