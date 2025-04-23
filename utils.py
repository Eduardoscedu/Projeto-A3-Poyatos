from tkinter import messagebox

def limpar_campos(entries):
    for entry in entries:
        entry.delete(0, "end")

def preencher_campos(event, entries, tree):
    selected = tree.selection()
    if selected:
        values = tree.item(selected, "values")
        for entry, val in zip(entries, values[1:]):
            entry.delete(0, "end")
            entry.insert(0, val)

def validar_campos(marca, modelo, ano, preco):
    if not all([marca, modelo, ano, preco]):
        messagebox.showwarning("Validação", "Todos os campos são obrigatórios.")
        return False

    if not isinstance(marca, str) or not isinstance(modelo, str):
        messagebox.showwarning("Validação", "Marca e Modelo devem ser texto.")
        return False

    try:
        int(ano)
    except ValueError:
        messagebox.showwarning("Validação", "Ano deve ser um número inteiro.")
        return False

    try:
        float(preco)
    except ValueError:
        messagebox.showwarning("Validação", "Preço deve ser um número decimal. (Ex. 19999.00)")
        return False

    return True

def formatar_preco(preco):
    try:
        return f"{float(preco):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except ValueError:
        return preco
