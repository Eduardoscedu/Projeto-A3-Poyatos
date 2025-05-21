# 🚗 Loja de Carros — Sistema de Gestão em Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/API-FIPE-blueviolet?style=for-the-badge" />
</p>

---

## 🎯 **Sobre o Projeto**

O **Loja de Carros** é um sistema de gestão de veículos com interface gráfica desenvolvido em **Python** utilizando **Tkinter**, **SQLite** e integração com a **API pública da Tabela FIPE**.

Permite o gerenciamento completo de estoque de carros, controle de vendas, pesquisa por veículos, além de registro e autenticação de usuários com diferentes níveis de acesso (Vendedor e Administrador).

---

## 📸 **Demonstração**

<p align="center">
  <img src="https://user-images.githubusercontent.com/yourimage.png" width="600"/>
</p>

---

## 🏗️ **Funcionalidades**

- 🔑 **Login e Registro com controle de acesso**
- 🚗 **Cadastro de carros** (marca, modelo, ano, preço)
- 🔍 **Pesquisa inteligente** com filtros
- ✏️ **Edição e atualização de informações dos veículos**
- 🗑️ **Remoção de veículos do estoque**
- 💰 **Venda de carros com cálculo de parcelamento**
- 📜 **Histórico de vendas registrado com o vendedor**
- 🌐 **Integração com a API da Tabela FIPE** para autocomplete de marcas e modelos

---

## 🗂️ **Estrutura do Projeto**

```plaintext
📦 loja-de-carros
├── main.py               # Ponto de entrada do programa
├── gui.py                # Interface gráfica (Tkinter)
├── database.py           # Gerenciamento do banco SQLite
├── utils.py              # Funções auxiliares
├── fipe_api.py           # Integração com API da Tabela FIPE
├── loja_carros.db        # Banco SQLite (gerado automaticamente)
├── Background_image.png  # Imagem de fundo da tela de login
└── README.md             # Documentação do projeto
