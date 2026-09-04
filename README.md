\# 🖥️ Inventário de TI



Sistema web para gerenciamento de equipamentos e ativos de Tecnologia da Informação, desenvolvido com Python, FastAPI e Streamlit.



O projeto nasceu como uma aplicação pessoal de estudo e evolução contínua, com foco em organização de código, separação de responsabilidades, desenvolvimento de APIs REST e criação de uma interface simples para operações de inventário.



\---



\## 📌 Sobre o projeto



O \*\*Inventário de TI\*\* permite controlar equipamentos de forma centralizada, oferecendo operações de cadastro, consulta, edição, remoção e exportação.



A aplicação foi estruturada para separar a interface do usuário da camada de API, permitindo que o projeto evolua futuramente para outras interfaces, como React, sem precisar reescrever a regra de negócio existente.



\### Objetivos



\- Centralizar o cadastro de equipamentos de TI.

\- Facilitar consultas e alterações no inventário.

\- Separar frontend, backend e regras de negócio.

\- Praticar desenvolvimento de APIs REST com FastAPI.

\- Praticar interfaces web com Streamlit.

\- Utilizar controle de versão com Git e GitHub.

\- Criar uma base preparada para futuras integrações.



\---



\## 🚀 Funcionalidades



\### 🔐 Autenticação



\- Login com usuário e senha.

\- Senha armazenada em formato de hash SHA-256.

\- Credenciais mantidas fora do código-fonte através do `secrets.toml`.

\- Estrutura preparada para futura evolução da autenticação.



\### 💻 Gestão de equipamentos



\- ✅ Cadastrar equipamento

\- ✅ Listar equipamentos

\- ✅ Editar equipamento

\- ✅ Remover equipamento

\- ✅ Exportar dados

\- ✅ Comunicação entre interface e API



\### 📋 Dados controlados



O inventário pode trabalhar com informações como:



\- Patrimônio

\- Tipo

\- Marca

\- Modelo

\- Número de série

\- Usuário/responsável

\- Setor

\- Status

\- Informações patrimoniais complementares



\---



\## 🏗️ Arquitetura



A aplicação utiliza uma arquitetura em camadas:



```text

┌─────────────────────────────┐

│          Navegador          │

└──────────────┬──────────────┘

&#x20;              │

&#x20;              ▼

┌─────────────────────────────┐

│         Streamlit           │

│        Interface Web        │

└──────────────┬──────────────┘

&#x20;              │ HTTP

&#x20;              ▼

┌─────────────────────────────┐

│          FastAPI            │

│         API REST            │

└──────────────┬──────────────┘

&#x20;              │

&#x20;              ▼

┌─────────────────────────────┐

│       Camada de Serviços    │

│        Regra de negócio     │

└──────────────┬──────────────┘

&#x20;              │

&#x20;              ▼

┌─────────────────────────────┐

│      Repository / Dados     │

└─────────────────────────────┘.



📁 Estrutura do projeto

inventario\_ti/

│

├── README.md

├── .gitignore

│

├── api/

│   ├── \_\_init\_\_.py

│   ├── dependencies.py

│   ├── main.py

│   ├── routes.py

│   └── schemas.py

│

├── cli/

│

├── exceptions/

│   ├── \_\_init\_\_.py

│   └── inventario\_exceptions.py

│

├── models/

│   ├── \_\_init\_\_.py

│   └── equipamento.py

│

├── repositories/

│   ├── \_\_init\_\_.py

│   └── equipamento\_repository.py

│

├── services/

│   ├── \_\_init\_\_.py

│   └── inventario\_service.py

│

├── streamlit\_app/

│   ├── api\_client.py

│   ├── app.py

│   ├── auth.py

│   ├── requirements.txt

│   └── .streamlit/

│       └── secrets.toml.example

│

├── tests/

│

├── inventario.json

└── requirements.txt

Responsabilidade das principais camadas

Camada	Responsabilidade

api/	Rotas, schemas e configuração da FastAPI

models/	Representação dos equipamentos

repositories/	Acesso e persistência dos dados

services/	Regras de negócio

exceptions/	Exceções específicas da aplicação

streamlit\_app/	Interface web e comunicação com a API

tests/	Testes automatizados

cli/	Operações via linha de comando

🛠️ Tecnologias

Backend

Python

FastAPI

Uvicorn

Frontend

Streamlit

Requests

Pandas

Versionamento

Git

GitHub

Possíveis evoluções



A arquitetura permite que o Streamlit seja futuramente substituído ou complementado por uma interface moderna utilizando:



React

TypeScript

Next.js



A API FastAPI pode continuar funcionando como backend principal.



⚙️ Requisitos



Antes de executar o projeto, tenha instalado:



Python

Git

Navegador web



Verifique as versões:



python --version

git --version

📥 Instalação



Clone o projeto:



git clone https://github.com/EstevanAnselmo/inventario-ti.git



Entre na pasta:



cd inventario-ti



Instale as dependências da API:



python -m pip install -r requirements.txt



Instale as dependências do Streamlit:



python -m pip install -r streamlit\_app\\requirements.txt

🔐 Configuração do Streamlit



O arquivo de credenciais real não deve ser versionado.



Crie:



streamlit\_app/.streamlit/secrets.toml



Utilize como referência:



streamlit\_app/.streamlit/secrets.toml.example



Exemplo:



\[api]

base\_url = "http://127.0.0.1:8000"



\[auth]

usuario = "admin"

senha\_sha256 = "HASH\_DA\_SENHA"



⚠️ Nunca publique secrets.toml contendo senhas, tokens, chaves de API ou outras credenciais.



▶️ Executando o projeto



O backend e o frontend são executados separadamente.



1\. Iniciar a API



Abra um PowerShell:



cd "C:\\caminho\\para\\inventario-ti"

python -m uvicorn api.main:app --reload



A API estará disponível em:



http://127.0.0.1:8000



Documentação interativa:



http://127.0.0.1:8000/docs

2\. Iniciar o Streamlit



Abra outro PowerShell:



cd "C:\\caminho\\para\\inventario-ti\\streamlit\_app"

python -m streamlit run app.py



A aplicação estará disponível em:



http://localhost:8501

🔄 Fluxo de comunicação

Usuário

&#x20;  │

&#x20;  ▼

Streamlit :8501

&#x20;  │

&#x20;  │ HTTP

&#x20;  ▼

FastAPI :8000

&#x20;  │

&#x20;  ▼

Services

&#x20;  │

&#x20;  ▼

Repository

&#x20;  │

&#x20;  ▼

Dados do inventário



O arquivo api\_client.py concentra as chamadas HTTP realizadas pelo Streamlit, mantendo a comunicação com a API separada da interface.



🔌 API



A API trabalha com o recurso:



/equipamentos



Operações principais:



GET    /equipamentos

POST   /equipamentos

PUT    /equipamentos/{id}

DELETE /equipamentos/{id}



A documentação interativa pode ser acessada em:



http://127.0.0.1:8000/docs

🧪 Testes



Os testes ficam organizados no diretório:



tests/



Antes de uma alteração importante, recomenda-se validar:



Inicialização da API.

Inicialização do Streamlit.

Login.

Cadastro.

Listagem.

Edição.

Remoção.

Exportação.

Comunicação entre frontend e backend.

🐛 Diagnóstico de problemas

API não conecta



Erro comum:



WinError 10061



Verifique se a API está rodando:



http://127.0.0.1:8000/docs

Erro 404



Possíveis causas:



Endpoint incorreto.

Rota não registrada.

URL incorreta no cliente.

Erro 422



Normalmente significa que os dados enviados não correspondem ao schema esperado pela API.



Erro 500



Indica uma falha interna no backend, regra de negócio ou persistência dos dados.



Erro no secrets.toml



Verifique:



streamlit\_app/.streamlit/secrets.toml



e confirme se as seções e chaves esperadas estão configuradas corretamente.



🌿 Controle de versão



O projeto utiliza Git e GitHub para controle de versão e sincronização entre ambientes de desenvolvimento.



Atualizar o projeto

git pull

Ver alterações

git status

Registrar uma alteração

git add .

git commit -m "Descricao da alteracao"

Enviar alterações

git push

Fluxo recomendado

git pull

&#x20;   ↓

Desenvolver

&#x20;   ↓

Testar

&#x20;   ↓

git status

&#x20;   ↓

git add .

&#x20;   ↓

git commit

&#x20;   ↓

git push

🔒 Segurança



O projeto mantém configurações sensíveis fora do código-fonte.



Arquivos que não devem ser versionados:



.streamlit/secrets.toml

.env

\_\_pycache\_\_/

\*.pyc

.venv/

venv/



O .gitignore é responsável por impedir que esses arquivos sejam adicionados ao repositório.



SHA-256 está sendo utilizado neste protótipo para a autenticação. Para um ambiente de produção, recomenda-se utilizar um mecanismo apropriado de password hashing, gerenciamento seguro de sessões e uma estratégia de autenticação adequada ao ambiente.



🗺️ Roadmap

Versão atual

&#x20;Autenticação

&#x20;Cadastro de equipamentos

&#x20;Listagem

&#x20;Edição

&#x20;Remoção

&#x20;Exportação

&#x20;API FastAPI

&#x20;Interface Streamlit

&#x20;Controle de versão com Git/GitHub

Próximas melhorias

&#x20;Dashboard inicial

&#x20;Pesquisa e filtros

&#x20;Melhorias visuais na tela de login

&#x20;Mostrar/ocultar senha

&#x20;Gestão de usuários

&#x20;Perfis e permissões

&#x20;Histórico de alterações

&#x20;Recuperação de senha

&#x20;Banco de dados dedicado

&#x20;Autenticação corporativa

&#x20;Ampliação dos testes automatizados

&#x20;Possível frontend React/TypeScript

📚 Objetivo educacional



Além de ser uma aplicação funcional, este projeto também serve como laboratório de aprendizado em desenvolvimento de software.



Principais conhecimentos praticados:



Python

APIs REST

FastAPI

Streamlit

Arquitetura em camadas

CRUD

Tratamento de exceções

Autenticação

Git

GitHub

Testes

Organização de projetos

Comunicação entre frontend e backend

👨‍💻 Autor



Estevan Anselmo



Projeto pessoal de estudo e desenvolvimento de software.



GitHub:



https://github.com/EstevanAnselmo



📄 Licença



Projeto desenvolvido para fins pessoais de estudo e desenvolvimento.



Uma licença específica poderá ser definida caso o projeto seja posteriormente distribuído ou disponibilizado publicamente.

