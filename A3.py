# CONECTA NO BANCO E CRIA TABELA (SEM VERIFICAR NADA)
import sqlite3

con = sqlite3.connect("banco_loja.db")
cur = con.cursor()
cur.execute("SELECT * FROM carr")
print(cur.fetchall())


def ad():
    print("Adicionar carro:")
    ma = input("Marca: ")
    mo = input("Modelo: ")
    an = input("Ano: ")
    pr = input("Preço: ")
    cur.execute("INSERT INTO carr (marca, modelo, ano, preco) VALUES ('" + ma + "','" + mo + "','" + an + "','" + pr + "')")
    con.commit()
    print("Carro adicionado\n")

def ve():
    print("Lista de carros:")
    cur.execute("SELECT * FROM carr")
    res = cur.fetchall()
    if not res:
        print("Nenhum carro cadastrado.\n")
    else:
        for x in res:
            print("ID:", x[0], "Marca:", x[1], "Modelo:", x[2], "Ano:", x[3], "Preço:", x[4])
        print("")


def ed():
    print("Editar carro")
    i = input("ID: ")
    m = input("Nova marca: ")
    md = input("Novo modelo: ")
    a = input("Novo ano: ")
    p = input("Novo preço: ")
    cur.execute("UPDATE carr SET marca='" + m + "', modelo='" + md + "', ano='" + a + "', preco='" + p + "' WHERE id=" + i)
    con.commit()
    print("Editado\n")

def rm():
    print("Remover carro")
    i = input("ID: ")
    cur.execute("DELETE FROM carr WHERE id=" + i)
    con.commit()
    print("Removido\n")

# MENU HORROROSO
while True:
    print("====== MENU DA LOJA ======")
    print("1 - Adicionar")
    print("2 - Ver")
    print("3 - Editar")
    print("4 - Remover")
    print("5 - Sair")
    op = input("Opcao: ")
    if op=="1":
        ad()
    elif op=="2":
        ve()
    elif op=="3":
        ed()
    elif op=="4":
        rm()
    elif op=="5":
        print("Falou!")
        break
    else:
        print("Opcao invalida man\n")
