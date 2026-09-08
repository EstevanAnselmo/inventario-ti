# 🖥️ Inventário de TI

Sistema web para gerenciamento de equipamentos e ativos de Tecnologia da Informação, desenvolvido com **Python, FastAPI e Streamlit**.

Projeto pessoal de estudo e desenvolvimento contínuo, criado com foco em organização de código, separação de responsabilidades, desenvolvimento de APIs REST e construção de uma interface web para controle de inventário.

---

## 📌 Sobre o projeto

O **Inventário de TI** permite cadastrar, consultar, editar, remover e exportar informações relacionadas a equipamentos de Tecnologia da Informação. Os registros presentes neste repositório são dados fictícios para demonstração.

A aplicação utiliza uma arquitetura separada em camadas, mantendo a interface desacoplada da API e das regras de negócio.

### Objetivos

* Centralizar informações dos equipamentos.
* Facilitar consultas e alterações no inventário.
* Praticar desenvolvimento de APIs REST.
* Aplicar conceitos de arquitetura em camadas.
* Praticar desenvolvimento de interfaces web.
* Utilizar Git e GitHub para controle de versão.
* Criar uma base preparada para futuras evoluções.

---

## 🚀 Funcionalidades

### 🔐 Autenticação

* Login com usuário e senha.
* Senha comparada por hash SHA-256 no protótipo local.
* Credenciais configuradas através do `secrets.toml`.
* Estrutura preparada para futuras melhorias de autenticação.

### 💻 Gestão de equipamentos

* ✅ Cadastrar equipamentos
* ✅ Listar equipamentos
* ✅ Editar equipamentos
* ✅ Remover equipamentos
* ✅ Exportar dados
* ✅ Comunicação entre Streamlit e FastAPI

### 📋 Informações cadastradas

O sistema trabalha com informações como:

* Patrimônio
* Tipo
* Marca
* Modelo
* Número de série
* Usuário
* Setor
* Status

---

## 🏗️ Arquitetura

```text
                    ┌───────────────────┐
                    │     Navegador     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Streamlit     │
                    │   Interface Web   │
                    └─────────┬─────────┘
                              │
                              │ HTTP
                              ▼
                    ┌───────────────────┐
                    │      FastAPI      │
                    │      API REST     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Services      │
                    │  Regra de negócio │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Repository      │
                    │ Persistência      │
                    └───────────────────┘
```

---

## 📁 Estrutura do projeto

```text
inventario_ti/
│
├── README.md
├── .gitignore
├── inventario.json
├── requirements.txt
│
├── api/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── cli/
│
├── exceptions/
│   ├── __init__.py
│   └── inventario_exceptions.py
│
├── models/
│   ├── __init__.py
│   └── equipamento.py
│
├── repositories/
│   ├── __init__.py
│   └── equipamento_repository.py
│
├── services/
│   ├── __init__.py
│   └── inventario_service.py
│
├── streamlit_app/
│   ├── app.py
│   ├── api_client.py
│   ├── auth.py
│   ├── requirements.txt
│   └── .streamlit/
│       └── secrets.toml.example
│
└── tests/
```

---

## 🧩 Organização das camadas

| Diretório        | Responsabilidade                      |
| ---------------- | ------------------------------------- |
| `api/`           | Rotas, schemas e configuração da API  |
| `models/`        | Modelos de dados                      |
| `repositories/`  | Persistência e acesso aos dados       |
| `services/`      | Regras de negócio                     |
| `exceptions/`    | Exceções personalizadas               |
| `streamlit_app/` | Interface web e comunicação com a API |
| `tests/`         | Testes                                |
| `cli/`           | Interface de linha de comando         |

---

## 🛠️ Tecnologias

### Backend

* Python
* FastAPI
* Uvicorn

### Frontend

* Streamlit
* Requests
* Pandas

### Versionamento

* Git
* GitHub

---

## ⚙️ Requisitos

Instalado no ambiente:

* Python
* Git
* Navegador web

Verifique:

```powershell
python --version
git --version
```

---

## 📥 Instalação

Clone o repositório:

```powershell
git clone https://github.com/EstevanAnselmo/inventario-ti.git
```

Entre na pasta:

```powershell
cd inventario-ti
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Depois:

```powershell
python -m pip install -r streamlit_app\requirements.txt
```

---

## 🔐 Configuração

Crie o arquivo:

```text
streamlit_app/.streamlit/secrets.toml
```

Utilize o arquivo abaixo como modelo:

```text
streamlit_app/.streamlit/secrets.toml.example
```

Exemplo:

```toml
[api]
base_url = "http://127.0.0.1:8000"

[auth]
usuario = "admin"
senha_sha256 = "HASH_DA_SENHA"
```

> ⚠️ O arquivo `secrets.toml` não deve ser enviado ao GitHub.

---

## ▶️ Executando a aplicação

### API

Abra um terminal:

```powershell
python -m uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Documentação:

```text
http://127.0.0.1:8000/docs
```

### Streamlit

Abra outro terminal:

```powershell
cd streamlit_app
python -m streamlit run app.py
```

Aplicação:

```text
http://localhost:8501
```

---

## 🔌 API

Principal recurso:

```text
/equipamentos
```

Operações:

```http
GET    /equipamentos
POST   /equipamentos
PATCH  /equipamentos/{patrimonio}
DELETE /equipamentos/{patrimonio}
```

A documentação interativa da API pode ser acessada através do Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Testes

A pasta `tests/` está reservada para a suíte de testes automatizados. No estado atual do projeto, as validações devem ser feitas manualmente até que os testes automatizados sejam adicionados.

Antes de publicar alterações, recomenda-se verificar:

* Inicialização da API
* Inicialização do Streamlit
* Login
* Cadastro
* Listagem
* Edição
* Remoção
* Exportação
* Comunicação entre frontend e backend

---

## 🐛 Diagnóstico

### API não conecta

Erro comum:

```text
WinError 10061
```

Verifique:

```text
http://127.0.0.1:8000/docs
```

Se a página não abrir, a API provavelmente não está executando.

### Erro 404

Pode indicar:

* endpoint incorreto;
* rota inexistente;
* URL incorreta.

### Erro 422

Indica normalmente que os dados enviados não correspondem ao schema esperado pela API.

### Erro 500

Indica erro interno no backend ou na persistência dos dados.

### Erro de `secrets.toml`

Verifique o arquivo:

```text
streamlit_app/.streamlit/secrets.toml
```

---

## 🌿 Git

Fluxo recomendado:

```powershell
git pull
```

Desenvolver e testar.

Depois:

```powershell
git status
git add .
git commit -m "Descricao da alteracao"
git push
```

### Fluxo

```text
git pull
   ↓
Desenvolver
   ↓
Testar
   ↓
git status
   ↓
git add .
   ↓
git commit
   ↓
git push
```

---

## 🔒 Segurança

O projeto mantém informações sensíveis fora do código.

Arquivos ignorados:

```text
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
.venv/
venv/
```

A autenticação atual utiliza SHA-256 como parte de um protótipo local. Para produção, recomenda-se migrar para um algoritmo apropriado para armazenamento de senhas (como Argon2 ou bcrypt), além de implementar sessões/tokens, gestão de usuários, permissões e proteção contra ataques de força bruta.

Para um ambiente de produção, a autenticação deverá evoluir para uma solução adequada de gerenciamento de senhas, sessões e usuários.

---

## 🗺️ Roadmap

### ✅ Atual

* [x] Login
* [x] Cadastro de equipamentos
* [x] Listagem
* [x] Edição
* [x] Remoção
* [x] Exportação
* [x] FastAPI
* [x] Streamlit
* [x] Git
* [x] GitHub

### 🔜 Próximas versões

* [ ] Dashboard
* [ ] Pesquisa e filtros
* [ ] Melhorias na tela de login
* [ ] Mostrar/ocultar senha
* [ ] Gestão de usuários
* [ ] Perfis e permissões
* [ ] Histórico de alterações
* [ ] Recuperação de senha
* [ ] Banco de dados dedicado
* [ ] Autenticação corporativa
* [ ] Ampliação dos testes
* [ ] Possível frontend React + TypeScript

---

## 📚 Objetivo educacional

Este projeto também funciona como laboratório de aprendizado em desenvolvimento de software.

Conhecimentos praticados:

* Python
* FastAPI
* Streamlit
* APIs REST
* CRUD
* Arquitetura em camadas
* Tratamento de exceções
* Autenticação
* Git
* GitHub
* Testes
* Comunicação entre frontend e backend

---

## 👨‍💻 Autor

**Estevan Anselmo**

Projeto pessoal de estudo e desenvolvimento de software.

GitHub:

https://github.com/EstevanAnselmo

---

## 📄 Licença

Projeto desenvolvido para fins pessoais de estudo e desenvolvimento.
