import sqlite3

DB_NAME = "banco_loja.db"

def criar_tabela():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                preco FLOAT NOT NULL
            )
        """)
        conn.commit()

def adicionar_carro(marca, modelo, ano, preco):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO carros (marca, modelo, ano, preco) VALUES (?, ?, ?, ?)",
                       (marca, modelo, ano, preco))
        conn.commit()

def listar_carros():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carros")
        return cursor.fetchall()

def remover_carro(carro_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carros WHERE id = ?", (carro_id,))
        conn.commit()

def editar_carro(carro_id, marca, modelo, ano, preco):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE carros SET marca = ?, modelo = ?, ano = ?, preco = ?
            WHERE id = ?
        """, (marca, modelo, ano, preco, carro_id))
        conn.commit()