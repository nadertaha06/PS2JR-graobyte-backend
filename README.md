# PS2JR-graobyte-backend

API REST desenvolvida em Flask para o backend do projeto GraoByte. Gerencia autenticação de usuários e CRUD de produtos, com controle de acesso baseado em roles (admin/funcionário) e armazenamento no MongoDB.

**Deploy:** https://ps2jr-graobyte-backend-production.up.railway.app

## Tecnologias

- **Python / Flask** — framework web
- **MongoDB / PyMongo** — banco de dados
- **Flask-JWT-Extended** — autenticação via JWT
- **Flask-CORS** — controle de origens
- **bcrypt** — hash de senhas

## Configuração

1. Clone o repositório e crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

| Variável | Descrição |
|---|---|
| `MONGO_URI` | URI de conexão com o MongoDB Atlas |
| `JWT_SECRET_KEY` | Chave secreta para assinar os tokens JWT |
| `CORS_ORIGINS` | Origens permitidas (separe por vírgula) |
| `FLASK_DEBUG` | `true` em desenvolvimento, `false` em produção |

3. Inicie o servidor:

```bash
flask run
```

## Autenticação

A API usa JWT Bearer Token. Inclua o header em todas as rotas protegidas:

```
Authorization: Bearer <token>
```

O token é obtido na rota `POST /auth/login`.

---

## Endpoints

### Auth — `/auth`

#### `POST /auth/login`
Autentica um usuário e retorna o token JWT.

**Body:**
```json
{
  "email": "usuario@email.com",
  "senha": "senha123"
}
```

**Resposta `200`:**
```json
{
  "token": "<jwt>",
  "role": "admin",
  "nome": "João"
}
```

**Erros:** `400` dados inválidos · `401` credenciais inválidas

---

#### `POST /auth/cadastrar-funcionario` `🔒 admin`
Cria um novo usuário com role `funcionario`.

**Body:**
```json
{
  "nome": "Maria",
  "email": "maria@email.com",
  "senha": "senha123"
}
```

**Resposta `201`:**
```json
{ "mensagem": "Funcionário cadastrado com sucesso" }
```

**Erros:** `400` dados inválidos ou e-mail já cadastrado · `403` acesso negado

---

#### `GET /auth/funcionarios` `🔒 admin`
Lista todos os funcionários cadastrados (sem expor a senha).

**Resposta `200`:**
```json
[
  { "_id": "...", "nome": "Maria", "email": "maria@email.com", "role": "funcionario" }
]
```

**Erros:** `403` acesso negado

---

#### `DELETE /auth/funcionarios/<id>` `🔒 admin`
Remove um funcionário pelo ID.

**Resposta `200`:**
```json
{ "mensagem": "Funcionário removido" }
```

**Erros:** `400` ID inválido · `403` acesso negado · `404` funcionário não encontrado

---

### Produtos — `/produtos`

Todas as rotas de produtos exigem autenticação (`🔒`).

#### `GET /produtos/` `🔒`
Lista todos os produtos.

**Resposta `200`:**
```json
[
  {
    "_id": "...",
    "nome": "Café Especial",
    "descricao": "Grão arábica",
    "preco": 45.90,
    "categoria": "cafe",
    "disponivel": true,
    "criado_em": "2024-01-01T00:00:00",
    "atualizado_em": "2024-01-01T00:00:00"
  }
]
```

---

#### `GET /produtos/<id>` `🔒`
Busca um produto pelo ID.

**Resposta `200`:** objeto do produto.

**Erros:** `404` produto não encontrado

---

#### `POST /produtos/` `🔒`
Cria um novo produto.

**Body:**
```json
{
  "nome": "Café Especial",
  "descricao": "Grão arábica",
  "preco": 45.90,
  "categoria": "cafe",
  "disponivel": true
}
```

> `descricao` e `disponivel` são opcionais (padrão: `""` e `true`).

**Resposta `201`:** objeto do produto criado.

---

#### `PUT /produtos/<id>` `🔒`
Atualiza os campos de um produto existente.

**Body:** qualquer subconjunto dos campos do produto.

**Resposta `200`:**
```json
{ "mensagem": "Produto atualizado" }
```

**Erros:** `404` produto não encontrado

---

#### `DELETE /produtos/<id>` `🔒`
Remove um produto pelo ID.

**Resposta `200`:**
```json
{ "mensagem": "Produto removido" }
```

**Erros:** `404` produto não encontrado
