# gui.py
# Interface gráfica principal do sistema

import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabelas, adicionar_carro, listar_carros, remover_carro, editar_carro
from database import autenticar_usuario, registrar_usuario, pesquisar_carro, buscar_carro_por_id
from utils import limpar_campos, preencher_campos, validar_campos, formatar_preco

def iniciar_gui():
    """Inicia toda a aplicação gráfica."""
    criar_tabelas()
    root = tk.Tk()
    root.title("Login - Loja de Carros")
    root.geometry("400x400")

    # Função para criar campos de entrada com placeholders
    def criar_entry_placeholder(parent, placeholder, show=None):
        entry = tk.Entry(parent, font=("Arial", 12))
        entry.insert(0, placeholder)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
                if show:
                    entry.config(show=show)

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")
                if show:
                    entry.config(show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.pack(pady=5)
        return entry

    # Tela de login
    def tela_login():
        limpar_tela()
        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 16)).pack(pady=10)
        usuario_entry = criar_entry_placeholder(frame, "Usuário")
        senha_entry = criar_entry_placeholder(frame, "Senha", show="*")

        def tentar_login():
            nome = usuario_entry.get()
            senha = senha_entry.get()
            if nome == "Usuário" or senha == "Senha":
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            resultado = autenticar_usuario(nome, senha)
            if resultado:
                tela_loja(nome, resultado[0])
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")

        tk.Button(frame, text="Login", command=tentar_login).pack(pady=10)
        tk.Button(frame, text="Registrar", command=tela_registro).pack()

    # Tela de registro
    def tela_registro():
        limpar_tela()
        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Label(frame, text="Registrar", font=("Arial", 16)).pack(pady=10)
        usuario_entry = criar_entry_placeholder(frame, "Usuário")
        senha_entry = criar_entry_placeholder(frame, "Crie sua senha", show="*")
        key_entry = criar_entry_placeholder(frame, "Digite a chave de acesso")

        def tentar_registro():
            nome = usuario_entry.get()
            senha = senha_entry.get()
            key = key_entry.get()
            if nome == "Usuário" or senha == "Crie sua senha" or key == "Digite a chave de acesso":
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            sucesso, mensagem = registrar_usuario(nome, senha, key)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                tela_login()
            else:
                messagebox.showerror("Erro", mensagem)

        tk.Button(frame, text="Registrar", command=tentar_registro).pack(pady=10)
        tk.Button(frame, text="Voltar", command=tela_login).pack()

    # Tela principal da loja
    def tela_loja(nome, nivel):
        limpar_tela()
        root.geometry("1120x480")
        root.title(f"Loja de Carros - {nome} ({nivel})")

        # Campos de entrada
        frame_inputs = tk.Frame(root)
        frame_inputs.pack(pady=10)

        labels = ["Marca", "Modelo", "Ano", "Preço"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(frame_inputs, text=label).grid(row=0, column=i, padx=5)
            entry = tk.Entry(frame_inputs)
            entry.grid(row=1, column=i, padx=5)
            entries.append(entry)

        # Botões de ação
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=5)

        def atualizar_lista():
            """Atualiza a lista de carros no TreeView."""
            for item in tree.get_children():
                tree.delete(item)
            for carro in listar_carros():
                carro_formatado = list(carro)
                carro_formatado[4] = formatar_preco(carro_formatado[4])
                tree.insert("", tk.END, values=carro_formatado)
            
        def atualizar_lista_pesq(carros):
            """Exibe os resultados da pesquisa no TreeView."""
            for item in tree.get_children():
                tree.delete(item)
            for carro in carros:
                carro_formatado = list(carro)
                carro_formatado[4] = formatar_preco(carro_formatado[4])
                tree.insert("", tk.END, values=carro_formatado)


        def on_add():
            valores = [entry.get() for entry in entries]
            if not validar_campos(*valores):
                return
            adicionar_carro(valores[0], valores[1], int(valores[2]), float(valores[3]))
            atualizar_lista_pesq()
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

        def on_sell():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um carro para Vender.")
                return
            carro_id = tree.item(selected, "values")[0]
            tela_vender(carro_id)

            #Tela de Vender o carros
        def tela_vender(carro_id):
            janela_vender = tk.Toplevel()
            janela_vender.title("Vender Carro")
            janela_vender.geometry("480x480")
            janela_vender.resizable(False, False)
            
            carro = buscar_carro_por_id(carro_id)
            
            car = ttk.Treeview(janela_vender, columns=("Marca", "Modelo", "Ano", "Preço"), show="headings", height=10)
            colunas = [("Marca", 110), ("Modelo", 110), ("Ano", 100), ("Preço", 110)]
            
            for nome, largura in colunas:
                car.heading(nome, text=nome)
                car.column(nome, anchor=tk.CENTER, width=largura)
            car.pack(pady=10, fill=tk.BOTH, expand=True)
            
            # Insere o carro na tabela se for encontrado
            if carro:
                carro_formatado = list(carro)
                carro_formatado[4] = formatar_preco(carro_formatado[4])
                car.insert("", tk.END, iid=carro[0], values=carro_formatado[1:])


            
        def on_search():
            valores = [entry.get() for entry in entries]
            marca, modelo, ano, preco = valores

            # Verifica ano e preco
            try:
                ano_int = int(ano) if ano else None
            except ValueError:
                messagebox.showerror("Erro", "Ano inválido.")
                return

            try:
                preco_float = float(preco) if preco else None
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido.")
                return

            carros_filtrados = pesquisar_carro(marca, modelo, ano_int, preco_float)
            if carros_filtrados:
                atualizar_lista_pesq(carros_filtrados)
            else:
                messagebox.showinfo("Resultado", "Nenhum carro encontrado com esses critérios.")

        # Botões
        if nivel == 'ADMINISTRADOR':
            tk.Button(frame_buttons, text="➕ Adicionar", width=12, command=on_add).grid(row=0, column=0, padx=5)
            tk.Button(frame_buttons, text="✏️ Editar", width=12, command=on_edit).grid(row=0, column=1, padx=5)
            tk.Button(frame_buttons, text="🗑️ Remover", width=12, command=on_delete).grid(row=0, column=2, padx=5)
            tk.Button(frame_buttons, text="🆑 Limpar Campos", width=12, command=lambda: limpar_campos(entries)).grid(row=0, column=3, padx=5)
            
        elif nivel == 'VENDEDOR':
            tk.Button(frame_buttons, text="💲 Vender", width=12, command=on_sell).grid(row=0, column=4, padx=5)
            tk.Button(frame_buttons, text="🔍 Pesquisar", width=12, command=on_search).grid(row=0, column=5, padx=5)
            tk.Button(frame_buttons, text="🆑 Limpar Campos", width=12, command=lambda: limpar_campos(entries)).grid(row=0, column=3, padx=5)

        # Tabela TreeView
        tree = ttk.Treeview(root, columns=("ID", "Marca", "Modelo", "Ano", "Preço"), show="headings", height=10)
        for col in ("ID", "Marca", "Modelo", "Ano", "Preço"):
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        tree.bind("<<TreeviewSelect>>", lambda e: preencher_campos(e, entries, tree))

        atualizar_lista()

    # Função para limpar a tela atual
    def limpar_tela():
        for widget in root.winfo_children():
            widget.destroy()

    tela_login()
    root.mainloop()
