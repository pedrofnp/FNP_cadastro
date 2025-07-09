# FNP Cadastro

Sistema de gerenciamento de contatos voltado para a Frente Nacional de Prefeitos (FNP).  
Permite controle de registros, exportações CSV, autenticação de usuários e painel administrativo com filtros por município e estado.

---

## ⚙️ Requisitos

- Python 3.8+
- Django 4.x ou 5.x
- SQLite3 (ou outro banco Django compatível)

---

## 🚀 Como rodar localmente

# Clone o projeto
git clone https://github.com/seu-usuario/FNP_cadastro.git
cd FNP_cadastro

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Crie o banco e migre
python manage.py migrate

# Crie o superusuário
python manage.py createsuperuser

# Rode o servidor local
python manage.py runserver

---

## 🗂️ Estrutura
base/                    # App principal
│
├── static/              # JS, CSS e imagens
│   └── js/
│   └── css/
│
├── templates/base/      # dash.html, etc.            
│       └── partials/    # navbar, sidebar, etc.
|
├── views.py             # Lógica das páginas
├── urls.py              # Rotas
├── forms.py             # Formulários
├── models.py            # Modelos

---

## 📁 Funcionalidades

Login/logout de usuários
Cadastro e edição de contatos
Dashboard com filtros por estado e município
Exportação de dados em CSV
Integração com Select2
Scripts separados em static/js/
CSS separados em static/css/

---

## 💡 Boas práticas utilizadas

Organização dos templates com partials/
Separação de static/ por tipo
Views organizadas em funções nomeadas
URLs com name= para uso nos templates
Uso de variáveis de contexto em todas as views

---

## 🛡️ Git

Branch principal: master
Branch de desenvolvimento: dev
Use git checkout -b minha-feature para criar uma nova branch