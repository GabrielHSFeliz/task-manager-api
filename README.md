# 📝 Task Manager API

API RESTful para gerenciamento de tarefas, com autenticação JWT e controle de permissão por usuário. Cada usuário só acessa e gerencia suas próprias tarefas.

## 🚀 Tecnologias

- **Python 3.12**
- **FastAPI** — framework web assíncrono
- **SQLAlchemy** — ORM para banco de dados
- **SQLite** — banco de dados
- **Pydantic** — validação de dados
- **JWT (python-jose)** — autenticação por token
- **Passlib + Bcrypt** — hash de senhas

## ✨ Funcionalidades

- Cadastro de usuários com senha criptografada (bcrypt)
- Login com geração de token JWT
- CRUD completo de tarefas (criar, listar, editar, deletar)
- Cada tarefa é vinculada ao usuário que a criou
- Rotas protegidas: apenas o dono de uma tarefa pode editá-la ou deletá-la
- Documentação interativa automática (Swagger UI)

## 📂 Estrutura do projeto
task-manager-api/
├── main.py              # Ponto de entrada da aplicação
├── database.py          # Configuração da conexão com o banco
├── models.py             # Modelos SQLAlchemy (User, Task)
├── schemas.py             # Schemas Pydantic (validação de entrada/saída)
├── security.py            # Hash de senha, geração e validação de JWT
└── routers/
├── auth.py            # Rotas de cadastro e login
└── tasks.py           # Rotas de CRUD de tarefas
## 🔧 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/GabrielHSFeliz/task-manager-api.git
cd task-manager-api
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie as tabelas do banco:
```bash
python create_db.py
```

5. Rode o servidor:
```bash
uvicorn main:app --reload
```

6. Acesse a documentação interativa em `http://127.0.0.1:8000/docs`

## 📌 Endpoints

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/register` | Cadastra um novo usuário | Não |
| POST | `/login` | Autentica e retorna um token JWT | Não |
| GET | `/users/me` | Retorna dados do usuário logado | Sim |
| POST | `/tasks` | Cria uma nova tarefa | Sim |
| GET | `/tasks` | Lista as tarefas do usuário logado | Sim |
| PUT | `/tasks/{task_id}` | Atualiza uma tarefa existente | Sim |
| DELETE | `/tasks/{task_id}` | Remove uma tarefa | Sim |

## 🧪 Como testar via curl

### 1. Cadastrar um usuário

```bash
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gabriel",
    "email": "gabriel@teste.com",
    "password": "senha123"
  }'
```

### 2. Fazer login e obter o token

```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gabriel@teste.com",
    "password": "senha123"
  }'
```

Resposta esperada:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Copie o valor de `access_token` e use nas próximas requisições, substituindo `<TOKEN>`.

### 3. Criar uma tarefa

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Revisar autenticacao JWT"
  }'
```

### 4. Listar as tarefas do usuário logado

```bash
curl -X GET "http://127.0.0.1:8000/tasks" \
  -H "Authorization: Bearer <TOKEN>"
```

### 5. Atualizar uma tarefa

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI - atualizado",
    "description": "Concluido"
  }'
```

### 6. Deletar uma tarefa

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1" \
  -H "Authorization: Bearer <TOKEN>"
```

## 🔐 Autenticação

Após o login, use o token retornado no header das requisições protegidas:
Authorization: Bearer <seu_token_aqui>****
## 🎯 Sobre o projeto

Este projeto foi desenvolvido como parte do meu portfólio, com foco em praticar conceitos essenciais de desenvolvimento backend: autenticação segura, modelagem de banco de dados relacional, validação de dados e organização de código em uma arquitetura escalável (separação de rotas em módulos).

## 👤 Autor

**Gabriel Henrique**
- GitHub: [@GabrielHSFeliz](https://github.com/GabrielHSFeliz)
