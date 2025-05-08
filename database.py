# database.py
# Responsável pelas operações no banco de dados (SQLite)

import sqlite3
from utils import vender_carro


def conectar_banco():
    """Cria uma conexão com o banco de dados SQLite."""
    return sqlite3.connect('loja_carros.db')

def criar_tabelas():
    """Cria as tabelas no banco de dados, se ainda não existirem."""
    conn = conectar_banco()
    cursor = conn.cursor()

    # Criação da tabela de carros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            nivel_acesso TEXT NOT NULL
        )
    ''')

    # Criação da tabela de chaves de acesso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys_acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            nivel_acesso TEXT NOT NULL
        )
    ''')

    # Inserção de chaves padrão (se ainda não existirem)
    keys_validas = [('123', 'VENDEDOR'), ('456', 'ADMINISTRADOR')]
    for key, nivel in keys_validas:
        cursor.execute("SELECT * FROM keys_acesso WHERE key = ?", (key,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO keys_acesso (key, nivel_acesso) VALUES (?, ?)", (key, nivel))

    conn.commit()
    conn.close()

# Operações para carros
def adicionar_carro(marca, modelo, ano, preco):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO carros (marca, modelo, ano, preco) VALUES (?, ?, ?, ?)", (marca, modelo, ano, preco))
    conn.commit()
    conn.close()

def listar_carros():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carros")
    carros = cursor.fetchall()
    conn.close()
    return carros


def remover_carro(carro_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carros WHERE id = ?", (carro_id,))
    conn.commit()
    conn.close()

    

def editar_carro(carro_id, marca, modelo, ano, preco):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE carros SET marca=?, modelo=?, ano=?, preco=? WHERE id=?",
        (marca, modelo, ano, preco, carro_id)
    )
    conn.commit()
    conn.close()

def pesquisar_carro(marca="", modelo="", ano=None, preco=None):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    query = "SELECT * FROM carros WHERE 1=1"
    params = []

    if marca:
        query += " AND marca LIKE ?"
        params.append(f"%{marca}%")
    if modelo:
        query += " AND modelo LIKE ?"
        params.append(f"%{modelo}%")
    if ano is not None:
        query += " AND ano = ?"
        params.append(ano)
    if preco is not None:
        query += " AND preco = ?"
        params.append(preco)

    cursor.execute(query, params)
    carros = cursor.fetchall()
    conn.close()
    return carros


# Operações para login/registro
def autenticar_usuario(nome, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel_acesso FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def registrar_usuario(nome, senha, key):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel_acesso FROM keys_acesso WHERE key = ?", (key,))
    resultado = cursor.fetchone()
    if resultado:
        nivel = resultado[0]
        try:
            cursor.execute("INSERT INTO usuarios (nome, senha, nivel_acesso) VALUES (?, ?, ?)", (nome, senha, nivel))
            conn.commit()
            return True, f"Registrado com acesso: {nivel}"
        except sqlite3.IntegrityError:
            return False, "Nome de usuário já existe."
    else:
        return False, "Key inválida."

def buscar_carro_por_id(carro_id):
    conn = sqlite3.connect("loja_carros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, marca, modelo, ano, preco FROM carros WHERE id = ?", (carro_id,))
    carro = cursor.fetchone()
    conn.close()
    return vender_carro(carro)
