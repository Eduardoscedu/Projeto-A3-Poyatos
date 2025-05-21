🚗 Loja de Carros - Sistema de Gestão
Sistema de gestão de uma loja de carros com interface gráfica desenvolvida em Python utilizando Tkinter, SQLite e integração com a API da Tabela FIPE para consulta de marcas e modelos de veículos.

📜 Descrição
O projeto simula uma loja de carros, permitindo que usuários realizem:

✅ Login e registro com controle de acesso (VENDEDOR e ADMINISTRADOR)

✅ Cadastro de veículos (marca, modelo, ano, preço)

✅ Pesquisa de veículos disponíveis na loja

✅ Venda de veículos com geração de parcelamento

✅ Controle de estoque (adicionar, editar e remover veículos)

✅ Histórico de vendas com registro do vendedor

✅ Sugestão automática de marcas e modelos através da API da FIPE

🗂️ Estrutura do Projeto
plaintext
Copiar
Editar
.
├── main.py             # Ponto de entrada principal do programa
├── gui.py              # Interface gráfica do sistema (Tkinter)
├── database.py         # Operações e manipulação do banco de dados SQLite
├── utils.py            # Funções auxiliares (validação, formatação, etc.)
├── fipe_api.py         # Integração com a API pública da Tabela FIPE
├── loja_carros.db      # Banco de dados SQLite (gerado automaticamente)
├── Background_image.png# Imagem de fundo da tela de login
└── README.md           # Documentação do projeto
🔧 Tecnologias Utilizadas
🐍 Python 3.x

🖼️ Tkinter (Interface gráfica)

🗄️ SQLite (Banco de dados local)

🌐 API Tabela FIPE (Consulta de marcas e modelos)

🎨 Pillow (PIL) (Manipulação de imagem no Tkinter)

🚀 Funcionalidades
Funcionalidade	Descrição
🔑 Login/Registro	Acesso restrito por perfil (Vendedor/Admin) com chave de acesso no registro.
🚗 Cadastro de Carros	Adicionar veículos com informações de marca, modelo, ano e preço.
🔍 Pesquisa	Busca de veículos por marca, modelo, ano ou preço.
✏️ Edição	Permite editar informações dos veículos.
🗑️ Remoção	Remove carros do estoque.
💰 Venda	Simula venda, gera opções de parcelamento e registra no histórico.
📜 Histórico de Vendas	Armazena vendas feitas e quem foi o vendedor.
🌐 Sugestões dinâmicas	Autocomplete de marcas e modelos via API FIPE.
