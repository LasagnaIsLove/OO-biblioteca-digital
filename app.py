from flask import Flask, render_template, redirect, request, session, url_for, flash, get_flashed_messages, abort
from package.user import Cliente, Funcionario
from package.biblioteca import Biblioteca
from package.utils import Utils
from package.cripto import Criptografia
import re

u = Utils()

app = Flask(__name__)
app.secret_key = "ado ado ado quem ta lendo é uma pessoa muito legal"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        indentification = request.form.get("indentification")
        password = request.form.get("password")
        
        user = None
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, indentification):
            user = u.checar_email(indentification)
        
        else:
            user = u.checar_codigo(indentification)
        
        if not user or Criptografia().descriptografar(user["password"]) != password:
            return render_template("login.html", error="Indentificação ou senha incorretos")
        
        session["user"] = user["first_name"]
        session["last_name"] = user["last_name"]
        session["email"] = user["email"]
        session["codigo"] = user["codigo"]
        session["funcionario"] = user.get("funcionario", False)
        session["admin"] = user.get("admin", False)
        if session["admin"]:
            session["cargo"] = "admin"
        
        elif session["funcionario"] and not session["admin"]:
            session["cargo"] = "funcionario"
            
        else:
            session["cargo"] = "cliente"
        return redirect("/home")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        cargo = request.form.get("cargo", "cliente")
        
        if password != confirm_password:
            return render_template("register.html", error="Senhas não coincidem")
        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return render_template("register.html", error="Formato de e-mail inválido")
        
        if cargo == "funcionario":
            if not session.get("codigo") or not session.get("admin"):
                return render_template("register.html", error="Apenas administradores podem cadastrar funcionários")
            
            novo_user = Funcionario(first_name, last_name, password, email)
            usuario = u.checar_email(novo_user.email)
            if usuario:
                if not usuario["funcionario"]:
                    novo_user.promover_conta_cliente()
                    return redirect("/login")
                
                else:
                    return render_template("register.html", error="E-mail já cadastrado e com permissão de funcionario")
                
            novo_user.gerar_cadastro()
            return redirect("/login")
        
        else:
            novo_user = Cliente(first_name, last_name, password, email)
            if u.checar_email(novo_user.email):
                return render_template("register.html", error="E-mail já cadastrado")
            
            novo_user.gerar_cadastro()
            return redirect("/login")
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    return render_template("home.html")

@app.route("/user/<codigo>")
def user_profile(codigo):
    if "user" not in session:
        return redirect(url_for("login"))
    
    if not session.get("codigo") == codigo:
        return render_template("user.html", error="Você não tem permissão para acessar este perfil") 
    
    return render_template("user.html")
    
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if not session.get("admin"):
        return render_template("home.html", error="Apenas administradores podem excluir contas de funcionários")
    
    if request.method == "POST":
        codigo = request.form.get("codigo")
        
        if u.checar_codigo(codigo):
            flash(codigo, "pop_up")
            return redirect(url_for("delete"))
        else:   
            return render_template("delete.html", error="Código não encontrado")
        
    flashes = get_flashed_messages(category_filter=["pop_up"])
    codigo = flashes[0] if flashes else None
    pop_up = bool(codigo)
    return render_template("delete.html", codigo=codigo, pop_up=pop_up)

@app.route("/excluir")
def excluir_conta():
    if "user" not in session:
        return redirect(url_for("login"))
    codigo = request.args.get("codigo")
    pc = request.args.get("propia_conta")
    if not codigo:
        abort(400)
    u.excluir_cadastro(codigo)
    if not session.get("admin"):
        return redirect("/logout")
    
    if not pc:
        return redirect("/home")
    
    return redirect("/logout")

@app.route("/search", methods=["GET", "POST"])
def search():
    livros = []
    if request.method == "POST":
        id = request.form.get("title")
        id_type = request.form.get("id_type")   
        disponivel = request.form.get("disponivel")
        livros = u.buscar_livro(id, id_type, disponivel)
        
    
        if not livros:
            return render_template("search.html", error="Nenhum livro encontrado")
        
    return render_template("search.html", livros=livros)

@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    l_ISBN = request.form.get("ISBN")
    livro = u.buscar_livro(id=l_ISBN, id_type="ISBN", disp_bool=False)
    livro = livro[0]
    
    if not livro["disponivel"]:
        print("Livro não disponivel")
        return False
    
    u.emprestar(livro["ISBN"], session["codigo"])
    
    return render_template("search.html", success="Livro reservado com sucesso")

@app.route("/incrementar", methods=["GET", "POST"])
def alterar_qtd():
    quantidade = request.form.get("quantidade")
    l_ISBN = request.form.get("ISBN-func")
    livro = u.buscar_livro(id=l_ISBN, id_type="ISBN", disp_bool=False)
    livro = livro[0]
    
    u.incrementar_livro(ISBN=l_ISBN, qtd=int(quantidade))
    return render_template("search.html", success=f"Quantidade de {livro["titulo"]} alterada para {quantidade} com sucesso")

@app.route("/excluir_livro", methods=["GET", "POST"])
def excluir_livro():
    l_ISBN = request.form.get("ISBN2")
    
    if not l_ISBN:
        print("Livro não encontrado no sistema")
        return False
    
    u.excluir_livro(l_ISBN)
    
    return render_template("search.html", success="Livro removido com sucesso")
    
@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))
    
    historico = u.historico(session["codigo"])
    
    if not historico:
        return render_template("history.html", error="Nenhum livro associado a conta encontrado")
    
    return render_template("history.html", historico=historico)

@app.route("/devolver", methods=["POST"])
def devolucao():
    if request.method == "POST":
        l_ISBN = request.form.get("ISBN")
        
        if u.devolver(session["codigo"], l_ISBN):
            print("Livro devolvido com sucesso")
    
    return redirect(url_for("history"))

@app.route("/register_book", methods=["GET", "POST"])
def registrar_livro():
    if not session["user"]:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        ano = request.form.get("ano")
        l_ISBN = request.form.get("ISBN")
        
        if Biblioteca().adicionar_livro(titulo, autor, ano, l_ISBN):
            return render_template("register_book.html", success="livro registrado com sucesso")
        
        return render_template("register_book.html", error="Erro ao registrar livro, por favor tente novamente.")
            
    return render_template("register_book.html")
        
      
        

if __name__ == "__main__":
    app.run(debug=True)