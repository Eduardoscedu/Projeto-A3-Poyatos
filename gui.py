# gui.py
# Interface gráfica principal do sistema

import tkinter as tk
import random
import string

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import bcrypt
from database import criar_tabelas, adicionar_carro, registrar_venda, listar_carros, remover_carro, editar_carro
from database import autenticar_usuario, registrar_usuario, pesquisar_carro, buscar_carro_por_id, buscar_hash_senha
from utils import limpar_campos, preencher_campos, validar_campos, formatar_preco
from fipe_api import listar_marcas, listar_modelos

nome_vendedor = None
marcas_carros = listar_marcas()
marcas_dict = {m['nome']: m['codigo'] for m in marcas_carros}


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
        root.title("Login - Loja de Carros")
        root.geometry("400x400")

        
        # Carrega imagem de fundo
        imagem_fundo = Image.open("Background_image.png")
        imagem_fundo = imagem_fundo.resize((400, 400))
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

        label_fundo = tk.Label(root, image=imagem_fundo_tk)
        label_fundo.image = imagem_fundo_tk
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # Label de título
        tk.Label(root, text="Login", font=("Arial", 16), fg="black", bg=root["bg"]).pack(pady=(30, 10))

        # Função para criar campos de entrada com placeholder
        def criar_entry_placeholder(placeholder, show=None):
            entry = tk.Entry(root, font=("Arial", 12), fg="grey", bg="white", relief="flat", justify="center", width=18)
            entry.insert(0, placeholder)

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


        # Campos de usuário e senha
        usuario_entry = criar_entry_placeholder("Usuário")
        senha_entry = criar_entry_placeholder("Senha", show="*")

        # Ação ao clicar em Login
        def tentar_login():
            nome = usuario_entry.get()
            senha_digitada = senha_entry.get()

            if nome == "Usuário" or senha_digitada == "Senha":
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            # Buscar o hash da senha no banco
            hash_salvo = buscar_hash_senha(nome)

            if hash_salvo:
                senha_ok = bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_salvo)
                if senha_ok:
                    global nome_vendedor
                    # Pega também o nível de acesso (mantendo o que já tinha)
                    resultado = autenticar_usuario(nome)  # Só retorna o nível, não precisa da senha
                    if resultado:
                        nome_vendedor = nome
                        tela_loja(nome, resultado[0])
                else:
                    # Senha incorreta
                    senha_entry.delete(0, tk.END)
                    senha_entry.insert(0, "Senha incorreta")
                    senha_entry.config(fg="red", show="")
            else:
                # Usuário não encontrado
                usuario_entry.delete(0, tk.END)
                usuario_entry.insert(0, "Usuario incorreto")
                usuario_entry.config(fg="red", show="")

                def limpar_hint_usuario(event):
                    if usuario_entry.get() == "Usuario incorreto":
                        usuario_entry.delete(0, tk.END)
                        usuario_entry.config(fg="black", show="")

                def limpar_hint_senha(event):
                    if senha_entry.get() == "Senha incorreta":
                        senha_entry.delete(0, tk.END)
                        senha_entry.config(fg="black", show="*")

                usuario_entry.bind("<FocusIn>", limpar_hint_usuario)
                senha_entry.bind("<FocusIn>", limpar_hint_senha)

        # Botões estilizados diretamente no root
        estilo_botao = {"bg": "white", "fg": "black", "relief": "flat", "font": ("Arial", 11, "bold"), "bd": 0}

        

        tk.Button(root, text="Login",  command=tentar_login, **estilo_botao).pack(pady=(10, 5), ipadx=10)
        tk.Button(root, text="Registrar", command=tela_registro, **estilo_botao).pack(ipadx=10)


    # Tela de registro
    def tela_registro():
        limpar_tela()
        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Label(frame, text="Registrar", font=("Arial", 16)).pack(pady=10)
        usuario_entry = criar_entry_placeholder(frame, "Usuário")
        senha_entry = criar_entry_placeholder(frame, "Crie sua senha", show="*")
        retry_senha_entry = criar_entry_placeholder(frame, "Repita sua senha", show="*")
        key_entry = criar_entry_placeholder(frame, "Digite a chave de acesso")

        def tentar_registro():
            nome = usuario_entry.get()
            senha = senha_entry.get()
            repetição_senha = retry_senha_entry.get()
            key = key_entry.get()
            if nome == "Usuário" or senha == "Crie sua senha" or key == "Digite a chave de acesso":
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            if senha != repetição_senha:
                messagebox.showerror("Erro", "Senhas diferentes!!.")
                return
            #Implementação do HASH
            senha_bytes = senha.encode('utf-8')
            salto = bcrypt.gensalt()
            hash_senha = bcrypt.hashpw(senha_bytes, salto)

            sucesso, mensagem = registrar_usuario(nome, hash_senha, key)
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
            if label == "Marca":
                entry_marca = tk.Entry(frame_inputs)
                entry_marca.grid(row=1, column=i, padx=5)
                entries.append(entry_marca)

                listbox_sugestoes = tk.Listbox(frame_inputs, height=5, width=15)
                listbox_sugestoes.grid(row=2, column=i, padx=5, pady=(5, 0))  # espaço superior de 05 pixels

            elif label == "Modelo":
                entry_modelo = tk.Entry(frame_inputs)
                entry_modelo.grid(row=1, column=i, padx=5)
                entries.append(entry_modelo)

                listbox_modelos = tk.Listbox(frame_inputs, height=5, width=18, font=("Arial", 9))
                listbox_modelos.grid(row=2, column=i, padx=5, pady=(5, 0))
                listbox_modelos.grid_remove()

                modelos_carregados = []  # manter fora das funções internas

                def atualizar_sugestoes_modelo(event):
                    texto_modelo = entry_modelo.get().lower()
                    listbox_modelos.delete(0, tk.END)
                    if texto_modelo:
                        sugeridas = [m for m in modelos_carregados if texto_modelo in m.lower()]
                        if sugeridas:
                            for modelo in sugeridas:
                                listbox_modelos.insert(tk.END, modelo)
                            listbox_modelos.grid()
                        else:
                            listbox_modelos.grid_remove()
                    else:
                        listbox_modelos.grid_remove()

                def selecionar_modelo(event):
                    selecionado = listbox_modelos.get(tk.ANCHOR)
                    entry_modelo.delete(0, tk.END)
                    entry_modelo.insert(0, selecionado)
                    listbox_modelos.grid_remove()

                entry_modelo.bind("<KeyRelease>", atualizar_sugestoes_modelo)
                listbox_modelos.bind("<<ListboxSelect>>", selecionar_modelo)


                listbox_sugestoes.grid_remove()  # Esconde inicialmente

                def atualizar_sugestoes_marca(event):
                    texto_marca = entry_marca.get().lower()
                    listbox_sugestoes.delete(0, tk.END)
                    if texto_marca:
                        #pega o nome de cada marca: m['nome'],
                        #Converte o nome para minúsculas: .lower()
                        #Verifica se o texto digitado (texto_marca) está dentro do nome
                        #E adiciona o nome (m['nome']) na lista sugeridas
                        sugeridas = [m['nome'] for m in marcas_carros if texto_marca in m['nome'].lower()]
                        if sugeridas:
                            for marca in sugeridas:
                                listbox_sugestoes.insert(tk.END, marca)
                            listbox_sugestoes.grid()  # Mostrar sugestões                            
                        else:
                            listbox_sugestoes.grid_remove()
                    else:
                        listbox_sugestoes.grid_remove()

                def selecionar_sugestao(event):
                    selecionado = listbox_sugestoes.get(tk.ANCHOR)
                    entry_marca.delete(0, tk.END)
                    entry_marca.insert(0, selecionado)
                    # Atualizar modelos com base na marca selecionada
                    marca_codigo = marcas_dict.get(selecionado)
                    if marca_codigo:
                        modelos = listar_modelos(marca_codigo)
                        modelos_carregados.clear()
                        modelos_carregados.extend([m['nome'] for m in modelos])
                    listbox_sugestoes.grid_remove()

                entry_marca.bind("<KeyRelease>", atualizar_sugestoes_marca)
                listbox_sugestoes.bind("<<ListboxSelect>>", selecionar_sugestao)

            else:
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
            letras_numeros = string.ascii_uppercase.replace("I", "").replace("O", "").replace("Q", "") + string.digits
            vin = ''.join(random.choices(letras_numeros, k=17))
            adicionar_carro(valores[0], valores[1], int(valores[2]), float(valores[3]), str(vin))
            atualizar_lista()
            messagebox.showinfo("Sucesso", "Carro inserido com sucesso.")
            limpar_campos(entries)
        
        def on_back():
            tela_login()

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
            janela_vender.geometry("480x500")
            janela_vender.resizable(False, False)

            carro = buscar_carro_por_id(carro_id)

            # Treeview sem a coluna de ID
            car = ttk.Treeview(
                janela_vender,
                columns=("Marca", "Modelo", "Ano", "Preço"),
                show="headings",
                height=10
            )

            colunas = [
                ("Marca", 70),
                ("Modelo", 70),
                ("Ano", 50),
                ("Preço", 70)
            ]

            for nome, largura in colunas:
                car.heading(nome, text=nome)
                car.column(nome, anchor=tk.CENTER, width=largura)

            car.pack(pady=10, fill=tk.BOTH, expand=True)

            if carro:
                carro_formatado = list(carro)
                preco_total = carro_formatado[4]
                chassi = carro_formatado[5]
                preco_formatado = formatar_preco(preco_total)

                valores = [
                    carro_formatado[1],  # Marca
                    carro_formatado[2],  # Modelo
                    carro_formatado[3],  # Ano
                    preco_formatado      # Preço
                ]

                preco_sem_formato = preco_formatado.split(',')[0].replace('.', '')
                preco = int(preco_sem_formato)

                car.insert("", tk.END, iid=carro[0], values=valores)

                # Listbox com opções de pagamento
                lista_parcelas = tk.Listbox(janela_vender, height=15, font=("Arial", 10))

                # ✅ Opção à vista
                lista_parcelas.insert(tk.END, f"À vista - {formatar_preco(preco_total)}")

                # Definindo parcelas com juros
                juros = 0.025  # 2,5% ao mês

                max_parcelas = 12 if preco <= 70000 else 24

                for i in range(2, max_parcelas + 1):
                    valor_total_com_juros = preco_total * ((1 + juros) ** i)
                    valor_parcela = valor_total_com_juros / i
                    lista_parcelas.insert(tk.END, f"{i}x de {formatar_preco(valor_parcela)}")

                lista_parcelas.pack(pady=10)

                # ✅ Função chamada quando uma opção da Listbox é selecionada
                def ao_selecionar_parcela(event):
                    selecao = lista_parcelas.curselection()
                    if selecao:
                        parcela_escolhida = lista_parcelas.get(selecao[0])

                        # Dados do carro
                        dados_carro = car.item(car.get_children()[0], "values")
                        marca, modelo, ano, preco = dados_carro

                        # Mensagem de confirmação
                        mensagem = (
                            f"🚗 Confirma a venda do carro: 🚗\n\n"
                            f"Marca: {marca}\n"
                            f"Modelo: {modelo}\n"
                            f"Ano: {ano}\n"
                            f"Preço à vista: {preco}\n\n"
                            f"Forma de pagamento selecionada: {parcela_escolhida}"
                        )

                        resposta = messagebox.askyesno("Confirmar Venda", mensagem)
                        if resposta:
                            messagebox.showinfo("Venda Realizada", f"Venda concluída com sucesso!")
                            remover_carro(carro_id)
                            atualizar_lista()

                            # Inserção no histórico
                            global nome_vendedor
                            registrar_venda(marca, modelo, ano, preco, nome_vendedor, chassi)
                            janela_vender.destroy()

                lista_parcelas.bind("<<ListboxSelect>>", ao_selecionar_parcela)

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
            tk.Button(frame_buttons, text="↩ Voltar", width=12, command=on_back).grid(row=0, column=0, padx=5)
            tk.Button(frame_buttons, text="➕ Adicionar", width=12, command=on_add).grid(row=0, column=1, padx=5)
            tk.Button(frame_buttons, text="✏️ Editar", width=12, command=on_edit).grid(row=0, column=2, padx=5)
            tk.Button(frame_buttons, text="🗑️ Remover", width=12, command=on_delete).grid(row=0, column=3, padx=5)
            tk.Button(frame_buttons, text="🆑 Limpar Campos", width=12, command=lambda: limpar_campos(entries)).grid(row=0, column=4, padx=5)
            
        elif nivel == 'VENDEDOR':
            tk.Button(frame_buttons, text="↩ Voltar", width=12, command=on_back).grid(row=0, column=0, padx=5)
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
