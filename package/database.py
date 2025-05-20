import os, json

class Database():
    def abrir_data(self, file):
        if os.path.exists(f"{file}.json"):
            with open(f"{file}.json", "r") as f:
                data = json.load(f)
            
        else:
            data = []
            
        return data
    
    def salvar_data(self, file, data):
        with open(f"{file}.json", "w") as f:
            json.dump(data, f, indent=4)
            
    def salvar_cadastro(self, cadastro):
        usuarios = self.abrir_data("users")
            
        usuarios.append(cadastro)
        
        self.salvar_data("users", usuarios)
        print(f"Cadastro salvo com sucesso.")
            
# db = Database() 
# db.salvar(usuarios)pipipi...popopo ;)d