# 📚 Biblioteca Digital – Aplicação Web em Flask

Este projeto implementa uma **biblioteca digital** utilizando **Python 3.12** e **Flask**, aplicando conceitos de **Programação Orientada a Objetos** (POO). Permite o cadastro, busca, empréstimo e devolução de livros, além de gerenciamento de usuários (Clientes e Funcionários).

---

## 🎯 Objetivos

- Demonstrar pilares da POO: **herança**, **polimorfismo**, **encapsulamento** e **modularização**.
- Simular operações de uma biblioteca digital real.
- Prover interface web simples e funcional.

---

## 🧩 Funcionalidades

- 🔎 **Busca de livros** por título, autor ou ISBN.
- 📚 **Cadastro de livros** (Funcionário).
- 👥 **Cadastro de usuários** (Clientes e Funcionários).
- 🔐 **Login** e **autenticação** de usuários.
- 📖 **Empréstimo** e **devolução** de livros.
- 📜 **Histórico** de empréstimos por usuário.
- 📊 **Controle de estoque** com atualização automática.

---

## 🧱 Estrutura do Projeto

```plain
OO-biblioteca-digital-main/
│
├── app.py                # Aplicação Flask (rotas e lógica de navegação)
├── biblioteca.json       # Banco de dados de livros (JSON)
├── users.json            # Banco de dados de usuários (JSON)
├── emprestimos.json      # Banco de dados de empréstimos (JSON)
├── package/              # Módulo com classes e utilitários
│   ├── biblioteca.py     # Classe Biblioteca (CRUD de livros)
│   ├── livro.py          # Classe Livro
│   ├── user.py           # Classes Usuario, Cliente, Funcionario
│   ├── database.py       # Gerenciamento de JSON como DB
│   ├── utils.py          # Funções auxiliares (Validações, Atualizações)
│   └── cripto.py         # Criptografia de senhas
├── templates/            # Páginas HTML (Jinja2)
│   ├── index.html        # Página inicial
│   ├── login.html        # Formulário de login
│   ├── register_book.html
│   ├── register_user.html
│   ├── loan_book.html
│   ├── return_book.html
│   └── history.html
├── static/               # Arquivos estáticos (CSS, JS, images)
│   ├── css/
│   └── js/
└── teste.py              # Script de testes (opcional)
```

---

## 📌 Casos de Uso

| Código | Caso de Uso          | Ator                | Descrição                               |
| ------ | -------------------- | ------------------- | --------------------------------------- |
| UC01   | Cadastrar Livro      | Funcionário         | Adiciona novos livros ao acervo         |
| UC02   | Buscar Livro         | Cliente/Funcionário | Pesquisa livros por critérios           |
| UC03   | Cadastrar Usuário    | Funcionário         | Registra novos clientes ou funcionários |
| UC04   | Login                | Cliente/Funcionário | Autentica acesso ao sistema             |
| UC05   | Realizar Empréstimo  | Cliente             | Empréstimo de livro disponível          |
| UC06   | Devolver Livro       | Cliente             | Devolve livro emprestado                |
| UC07   | Visualizar Histórico | Cliente             | Exibe histórico de empréstimos          |

---

## ⚙️ Requisitos

- Python 3.12
- Flask (pip install flask)

---

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/LasagnaIsLove/OO-biblioteca-digital.git
   cd OO-biblioteca-digital-main
   ```

2. Instale o Flask:

   ```bash
   pip install flask
   ```

3. Execute a aplicação:

   ```bash
   python app.py
   ```

4. Abra no navegador:

   ```
   http://localhost:5000
   ```

---

## 📄 Tecnologias

- Linguagem: **Python 3.12**
- Framework Web: **Flask**
- Banco de dados: arquivos **JSON** (simples e sem dependências externas)
- Templates: **Jinja2**

---

## 🧠 Diagrama de Classes

```mermaid
classDiagram
    class Biblioteca {
        - livros : list<Livro>
        - usuarios : list<Usuario>
        + adicionar_livro()
        + buscar_livro()
        + emprestar_livro(livroISBN, usuarioID)
        + devolver_livro(livroISBN, usuarioID)
        + carregar_dados()
        + salvar_dados()
    }
    class Livro {
        - titulo : str
        - autor : str
        - isbn : str
        - ano : int
        - editora : str
        - disponivel : bool
        + to_dict() : dict
    }
    class Usuario {
        - nome : str
        - matricula : str
        - email : str
        - senha_hash : str
        + autenticar(senha : str) : bool
    }
    class Cliente {
        + emprestar(livroISBN : str) : bool
        + devolver(livroISBN : str) : bool
    }
    class Funcionario {
        + cadastrar_livro(livro : Livro) : None
        + cadastrar_usuario(usuario : Usuario) : None
    }
    class Database {
        + load(arquivo : str) : dict
        + save(arquivo : str, dados : dict) : None
    }
    class Cripto {
        + hash_password(senha : str) : str
        + check_password(senha : str, hash : str) : bool
    }

    Biblioteca "1" o-- "*" Livro
    Biblioteca "1" o-- "*" Usuario
    Usuario <|-- Cliente
    Usuario <|-- Funcionario
    Biblioteca ..> Database : utiliza
    Usuario ..> Cripto : utiliza
```

---

## 📝 Licença

Projeto destinado a fins educacionais. Não possui licença específica.

---

*Desenvolvido para disciplina de Orientação a Objetos*
