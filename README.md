# OO-biblioteca-digital
  Este projeto foi desenvolvido como parte da disciplina de Orientação a Objetos e tem como objetivo simular o funcionamento básico de uma biblioteca digital, permitindo o cadastro, login, empréstimo e devolução de livros por usuários autenticados.

## ✅ Objetivo do Projeto
  O sistema visa proporcionar uma experiência simples e funcional para gerenciamento de livros e empréstimos, usando conceitos de orientação a objetos como herança, polimorfismo, encapsulamento e modularização.

## 🧱 Estrutura do Projeto
```
biblioteca-digital/
  ├── 📄 README.md
  ├── 🧠 main.py
  └── 📦 package/
    ├── 📘 livro.py
    ├── 👤 usuario.py
    ├── 🔁 emprestimo.py
    ├── 🏛️ biblioteca.py
    └── 🧩 mixins.py
```

- **main.py**: ponto de entrada do programa.
- **package/**: pacote com todas as classes do sistema, organizadas por responsabilidade.

---

## 🧩 Funcionalidades

- Cadastro e busca de livros
- Cadastro de usuários (alunos e funcionários)
- Login de usuários
- Empréstimo e devolução de livros
- Histórico de empréstimos
- Controle de disponibilidade dos livros

---

## 👥 Casos de Uso

### UC01 – Cadastrar Livro
- **Ator:** Funcionário
- Permite que o funcionário cadastre um novo livro no sistema.

### UC02 – Buscar Livro
- **Ator:** Aluno ou Funcionário
- Permite pesquisar livros pelo título, autor ou ISBN.

### UC03 – Cadastrar Usuário
- **Ator:** Funcionário
- Permite cadastrar um novo usuário do sistema (aluno ou funcionário).

### UC04 – Realizar Login
- **Ator:** Aluno ou Funcionário
- Permite que o usuário entre no sistema usando matrícula e senha.

### UC05 – Realizar Empréstimo
- **Ator:** Aluno
- Permite que o aluno realize o empréstimo de um livro disponível.

### UC06 – Devolver Livro
- **Ator:** Aluno
- Permite a devolução de um livro previamente emprestado.

### UC07 – Visualizar Histórico
- **Ator:** Aluno
- Exibe o histórico de empréstimos do usuário.

---

## 📐 Diagrama de Classes (Descrição Textual)

### Classes Principais:

- **Livro**
  - Atributos: título, autor, ISBN, ano, editora, status
- **Usuario** *(abstrata)*
  - Subclasses: `Aluno`, `Funcionario`
  - Atributos: nome, matrícula, email
- **Emprestimo**
  - Atributos: livro, usuario, data_emprestimo, data_devolucao, devolvido
- **Biblioteca**
  - Métodos: adicionar_livro(), buscar_livro(), registrar_emprestimo(), registrar_devolucao(), listar_historico()

### Relacionamentos e Conceitos Aplicados:
- Herança: `Aluno` e `Funcionario` herdam de `Usuario`
- Polimorfismo: métodos como `exibir_perfil()` implementados de forma distinta em subclasses
- Composição forte: `Biblioteca` contém listas de `Livro` e `Emprestimo`
- Associação fraca: `Emprestimo` vincula `Usuario` e `Livro`
- Mixin: `PesquisavelMixin` adiciona métodos reutilizáveis para busca

---

## 💻 Tecnologias Utilizadas

- Python 3.12
- Programação orientada a objetos (POO)
- Interface de linha de comando (CLI) para testes

