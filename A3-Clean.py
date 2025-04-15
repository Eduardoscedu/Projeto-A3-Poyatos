import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "banco_loja.db"

def criar_tabela():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano TEXT NOT NULL,
                preco TEXT NOT NULL
            )
        """)
        conn.commit()

def adicionar_carro(marca, modelo, ano, preco, tree):
    if not (marca and modelo and ano and preco):
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO carros (marca, modelo, ano, preco) VALUES (?, ?, ?, ?)",
                       (marca, modelo, ano, preco))
        conn.commit()
    atualizar_lista(tree)
    messagebox.showwarning("Aviso", "Carro Inserido com sucesso!.")
    limpar_campos()

def atualizar_lista(tree):
    for item in tree.get_children():
        tree.delete(item)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carros")
        for carro in cursor.fetchall():
            tree.insert("", tk.END, values=carro)

def remover_carro(tree):
    item = tree.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um carro para remover.")
        return

    carro_id = tree.item(item, "values")[0]
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carros WHERE id = ?", (carro_id,))
        conn.commit()
        messagebox.showwarning("Aviso", "Remoção Realizada!.")
    atualizar_lista(tree)

def editar_carro(tree, marca, modelo, ano, preco):
    item = tree.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um carro para editar.")
        return

    carro_id = tree.item(item, "values")[0]
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE carros SET marca = ?, modelo = ?, ano = ?, preco = ?
            WHERE id = ?
        """, (marca, modelo, ano, preco, carro_id))
        conn.commit()
    atualizar_lista(tree)
    messagebox.showwarning("Aviso", "Modificação Feita!.")
    limpar_campos()

def preencher_campos(event, entries, tree):
    selected = tree.selection()
    if selected:
        values = tree.item(selected, "values")
        for entry, val in zip(entries, values[1:]):
            entry.delete(0, tk.END)
            entry.insert(0, val)

def limpar_campos():
    for entry in entries:
        entry.delete(0, tk.END)

# GUI
criar_tabela()
root = tk.Tk()
root.title("Loja de Carros - CRUD")
root.geometry("1120x480")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

labels = ["Marca", "Modelo", "Ano", "Preço"]
entries = []
for i, label in enumerate(labels):
    tk.Label(frame_inputs, text=label).grid(row=0, column=i, padx=5)
    entry = tk.Entry(frame_inputs)
    entry.grid(row=1, column=i, padx=5)
    entries.append(entry)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

btn_add = tk.Button(frame_buttons, text="Adicionar", width=12,
                    command=lambda: adicionar_carro(entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), tree))

btn_edit = tk.Button(frame_buttons, text="Editar", width=12,
                     command=lambda: editar_carro(tree, entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get()))

btn_del = tk.Button(frame_buttons, text="Remover", width=12,
                    command=lambda: remover_carro(tree))

btn_clear = tk.Button(frame_buttons, text="Limpar Campos", width=12, command=limpar_campos)

btn_add.grid(row=0, column=0, padx=5)
btn_edit.grid(row=0, column=1, padx=5)
btn_del.grid(row=0, column=2, padx=5)
btn_clear.grid(row=0, column=3, padx=5)

tree = ttk.Treeview(root, columns=("ID", "Marca", "Modelo", "Ano", "Preço"), show="headings", height=10)
for col in ("ID", "Marca", "Modelo", "Ano", "Preço"):
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree.pack(pady=10, fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", lambda e: preencher_campos(e, entries, tree))

atualizar_lista(tree)
root.mainloop()
