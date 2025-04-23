import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabela, adicionar_carro, listar_carros, remover_carro, editar_carro
from utils import limpar_campos, preencher_campos, validar_campos
from utils import validar_campos, formatar_preco

def iniciar_gui():
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

    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)
        for carro in listar_carros():
            carro_formatado = list(carro)
            carro_formatado[4] = formatar_preco(carro_formatado[4])
            tree.insert("", tk.END, values=carro_formatado)
    

    def on_add():
        valores = [entry.get() for entry in entries]
        if not validar_campos(*valores):
            return
        adicionar_carro(valores[0], valores[1], int(valores[2]), float(valores[3]))
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Carro inserido com sucesso.")
        limpar_campos(entries)

    def on_edit():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um carro para editar.")
            return
        valores = [entry.get() for entry in entries]
        if not validar_campos(*valores):
            return
        carro_id = tree.item(selected, "values")[0]
        editar_carro(carro_id, valores[0], valores[1], int(valores[2]), float(valores[3]))
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Carro editado com sucesso.")
        limpar_campos(entries)

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um carro para remover.")
            return
        carro_id = tree.item(selected, "values")[0]
        remover_carro(carro_id)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Carro removido.")

    btn_add = tk.Button(frame_buttons, text="➕ Adicionar", width=12, command=on_add)
    btn_edit = tk.Button(frame_buttons, text="✏️ Editar", width=12, command=on_edit)
    btn_del = tk.Button(frame_buttons, text="🗑️ Remover", width=12, command=on_delete)
    btn_clear = tk.Button(frame_buttons, text="🆑 Limpar Campos", width=12, command=lambda: limpar_campos(entries))

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

    atualizar_lista()
    root.mainloop()