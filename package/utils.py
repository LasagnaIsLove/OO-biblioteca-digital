from package.database import Database

class Utils(Database):        
    def checar_email(self, email):
        usuarios = Database().abrir_data("users")
                
        for usuario in usuarios:
            if usuario["email"] == email:
                return usuario
        return False

        
    def checar_codigo(self, codigo):
        usuarios = Database().abrir_data("users")
        
        for usuario in usuarios:
            if usuario["codigo"] == codigo:
                return usuario
        return False
        
    def excluir_cadastro(self, codigo):
        usuarios = Database().abrir_data("users")

        check = False
        for usuario in usuarios:
            if usuario["codigo"] == codigo:
                check = True
                print(f"Cadastro de {usuario["first_name"]} {usuario["last_name"]} excluído com sucesso.")
                usuarios.remove(usuario)
                break
            
        if check == False:
            print("Cadastro não encontrado.") 
        
        Database().salvar_data("users", usuarios)
        
    def normalizar (self, texto):
        acentos = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 
            'í': 'i', 'ì' : 'i', 'î': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u',
            'ç': 'c'
        }
        
        pontuacoes = ['.', ',', '!', '?', ';', ':', '-', '_', '(', ')', '"', "'", '/', '~', '^', '´', '`']
        
        if type(texto) != str:
            print("Error: texto inserido não é uma string")
            return False
        
        texto = texto.lower()
        texto_normal = ""
        espaco = False
        for char in texto:
            if char in acentos:
                texto_normal += acentos[char]
                
            elif char in pontuacoes:
                pass
            
            elif char == " ":
                if not espaco:
                    texto_normal += char
                    espaco = True
                
            else:
                texto_normal += char
                espaco = False
                
        return texto_normal
                
    def buscar_livro(self, id, id_type, disp_bool):
        self.atualizar_estoque()
        id_normal = self.normalizar(id)
        livros = Database().abrir_data("biblioteca")
        
        livros_encontrados = []
        if disp_bool:
            for l in livros:
                if l["disponivel"]:
                    if id_type == "titulo" and id_normal in self.normalizar(l["titulo"]):
                        livros_encontrados.append(l)
                        
                    if id_type == "autor" and id_normal in self.normalizar(l["autor"]):
                        livros_encontrados.append(l)
                        
                    if id_type == "ano" and str(id) in str(l["ano"]):
                        livros_encontrados.append(l)
                        
                    if id_type == "ISBN" and id in l["ISBN"]:
                        livros_encontrados.append(l)
                        
        else:
            for l in livros:
                if id_type == "titulo" and id_normal in self.normalizar(l["titulo"]):
                    livros_encontrados.append(l)
                    
                if id_type == "autor" and id_normal in self.normalizar(l["autor"]):
                    livros_encontrados.append(l)
                    
                if id_type == "ano" and str(id) in str(l["ano"]):
                    livros_encontrados.append(l)
                    
                if id_type == "ISBN" and id in l["ISBN"]:
                    livros_encontrados.append(l)
            
        return livros_encontrados
    
    def atualizar_estoque(self):
        livros = Database().abrir_data("biblioteca")
        
        for l in livros:
            if l["quantidade"] > 0:
                l["disponivel"] = True
            
            else:
                l["disponivel"] = False      
        
        Database().salvar_data("biblioteca", livros)
    
    def incrementar_livro(self, ISBN, qtd):
        livros = Database().abrir_data("biblioteca")
        print(ISBN)
        for l in livros:
            print(l)
            if l["ISBN"] == ISBN:
                print(l)
                livro = l
                break
                
        if not livro:
            print("livro não encontrado.")
            return False
        
        livro["quantidade"] = qtd
        
        if livro["quantidade"] < 0:
            print("Quantidade insuficiente par devolução")
            return False
        
        Database().salvar_data("biblioteca", livros) 
        self.atualizar_estoque()               
        return True
        
    
    def emprestar(self, l_ISBN , codigo_user, qtd=1):
        user = self.checar_codigo(codigo_user)
        
        livros = Database().abrir_data("biblioteca")
        
        
        for l in livros:
            if l["ISBN"] == str(l_ISBN):
                livro = l
                break
            
        if user:
            livro["quantidade"] -= int(qtd)
            
            if livro["quantidade"] < 0:
                print("Quantidade insuficiente para emprestar.")
                livro["quantidade"] += int(qtd)
                return False
        
            print(f"{qtd} cópia(s) de {livro["titulo"]} emprestada(s) com sucesso.")                
            
            Database().salvar_data("biblioteca", livros)
            
            self.atualizar_estoque()
                
            emprestimos = Database().abrir_data("emprestimos")
            
            emprestimo = {
                "nome" : user["first_name"] + " " + user["last_name"],
                "codigo" : codigo_user,
                "livro" : livro["titulo"],
                "ISBN" : livro["ISBN"],
                "quantidade" : qtd
            }
            
            emprestimos.append(emprestimo)
            
            Database().salvar_data("emprestimos", emprestimos)
                        
            return True
        
        print("Usuario não encontrado, por favor verifique os dados colocados.")
        return False

    def devolver(self, codigo_user, ISBN, qtd=1):
        emprestimos = Database().abrir_data("emprestimos")
        check = False
        for e in emprestimos:
            if e["codigo"] == codigo_user and e["ISBN"] == ISBN:
                emprestimo = e
                l_ISBN = e["ISBN"]
                check = True
                break
            
        if not check:
            print("nenhum emprestimo encontrado")
            return False
            
        emprestimos.remove(emprestimo)
        
        if self.incrementar_livro(l_ISBN, qtd):
            print(f"{qtd} cópias de {e["livro"]} devolvidas com sucesso.")
            Database().salvar_data("emprestimos", emprestimos)
            return True
            
        print("Quantidade inválida.")
        return False
    
    def excluir_livro(self, ISBN):
        livros = Database().abrir_data("biblioteca")
        for livro in livros:
            if livro["ISBN"] == ISBN:
                livro = livro
                break
        
        if livro in livros:
            print(livro)
            livros.remove(livro)
            Database().salvar_data("biblioteca", livros)
            return True
        
        print("livro não encontrado")
        return False
    
    def historico(self, codigo):
        emprestimos = Database().abrir_data("emprestimos")
        emprestimos_encotrados = []
        for e in emprestimos:
            if e["codigo"] == codigo:
                emprestimos_encotrados.append(e)
                
        if emprestimos_encotrados == []:
            print("nenhum empestimo encotrado.")
            return False
        
        return emprestimos_encotrados
                
            
        
        
                    
                
                
                