import sqlite3


DB_PATH = 'loja_carros.db'


def conectar_banco():
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            preco REAL NOT NULL,
            chassi TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            hash_senha TEXT NOT NULL,
            nivel_acesso TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys_acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            nivel_acesso TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            preco REAL NOT NULL,
            chassi TEXT,
            id_vendedor INTEGER,
            FOREIGN KEY (id_vendedor) REFERENCES usuarios(id)
        )
    ''')

    keys_validas = [('123', 'VENDEDOR'), ('456', 'ADMINISTRADOR')]
    for key, nivel in keys_validas:
        cursor.execute("SELECT * FROM keys_acesso WHERE key = ?", (key,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO keys_acesso (key, nivel_acesso) VALUES (?, ?)", (key, nivel))

    conn.commit()
    conn.close()


def adicionar_carro(marca, modelo, ano, preco, vin):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO carros (marca, modelo, ano, preco, chassi) VALUES (?, ?, ?, ?, ?)",
                   (marca, modelo, ano, preco, vin))
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


def autenticar_usuario(nome):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel_acesso FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def registrar_usuario(nome, hash_senha, key):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel_acesso FROM keys_acesso WHERE key = ?", (key,))
    resultado = cursor.fetchone()
    if resultado:
        nivel = resultado[0]
        try:
            cursor.execute("INSERT INTO usuarios (nome, hash_senha, nivel_acesso) VALUES (?, ?, ?)",
                           (nome, hash_senha, nivel))
            conn.commit()
            return True, f"Registrado com acesso: {nivel}"
        except sqlite3.IntegrityError:
            return False, "Nome de usuário já existe."
    else:
        return False, "Key inválida."
    conn.close()


def buscar_carro_por_id(carro_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, marca, modelo, ano, preco, chassi FROM carros WHERE id = ?", (carro_id,))
    carro = cursor.fetchone()
    conn.close()
    return carro


def registrar_venda(marca, modelo, ano, preco, nome_vendedor, chassi):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (nome_vendedor,))
    id_vendedor = cursor.fetchone()
    if id_vendedor:
        id_vendedor = id_vendedor[0]
        cursor.execute(
            "INSERT INTO historico (marca, modelo, ano, preco, chassi, id_vendedor) VALUES (?, ?, ?, ?, ?, ?)",
            (marca, modelo, ano, preco, chassi, id_vendedor)
        )
    conn.commit()
    conn.close()


def buscar_hash_senha(nome):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT hash_senha FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0]
    return None
