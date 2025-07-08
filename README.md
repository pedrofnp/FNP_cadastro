# 📇 Projeto Django - Sistema de Contatos FNP

Sistema para cadastro, filtragem e gerenciamento de contatos (prefeituras e representantes), com base nos dados da Frente Nacional de Prefeitas e Prefeitos (FNP).

---

## 🚀 Tecnologias Utilizadas

- Python 3.13
- Django 5.2
- Bootstrap 5
- Select2 (filtros avançados)
- SQLite (padrão)
- JavaScript / JQuery

---

## 📦 Estrutura do Projeto

contatos/
├── base/
│ ├── templates/base
│ │ ├── dash.html
│ │ └── partials/
│ │ │ ├── filters.html
│ │ │ └── table.html
│ ├── static/
│ │ ├── js/
│ │ └── styles/
│ ├── views.py
│ ├── models.py
│ ├── urls.py
│ └── forms.py
├── media/
│ └── fotos_perfil/
├── manage.py
└── db.sqlite3

## 📌 Funcionalidades

- Cadastro completo de contatos (nome, email, telefone, cargo, estado, município, partido, etc.)
- Upload de foto
- Sistema de filtros combinados (por estado, município, capital, interesse, etc.)
- Paginação dos resultados
- Edição e exportação de dados
- Integração com biblioteca Select2 para multiselect com Bootstrap 5
- Responsividade com Bootstrap

---

## 🛠️ Como Rodar Localmente

1. Clone o Projeto

   ```bash
   git clone https://github.com/usuario/repositorio.git
   cd repositorio

   ```

2. Crie e ative um ambiente virtual
   bash
   Copiar código
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate # Windows

3. Instale as dependências
   pip install -r requirements.txt

4. Rode o servidor
   python manage.py runserver

5. Acesse: http://127.0.0.1:8000/

 ## 📂 Organização dos Templates
    dash.html: página principal com layout e carregamento de componentes

    partials/filters.html: formulário de filtros

    partials/table.html: listagem com paginação

 ## 📂 Organização dos Arquivos Estáticos
    static/js/: JavaScript modular (dashboard.js, filtros, AJAX, etc.)

    static/styles/: CSS customizados (sidebars, bootstrap, filtros)

    static/images/: imagens e ícones

    Todos os arquivos estáticos são incluídos nos templates com {% load static %} e src="{% static 'caminho/do/arquivo' %}".

 ##  🔍 Observações
    O CSS e JS foram corretamente separados em arquivos externos.

    O campo de municípios é populado dinamicamente via fetch() a partir do estado_id.

    Projeto está em processo de refatoração com foco em boas práticas, organização e manutenção futura.

  ##  ⚖️ Licença

Todos os direitos reservados à Frente Nacional de Prefeitas e Prefeitos (FNP).
