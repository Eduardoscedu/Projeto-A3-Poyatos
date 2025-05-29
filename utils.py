# utils.py
# Funções auxiliares para a interface gráfica

from logging import root
from tkinter import messagebox, ttk

def limpar_campos(entries):
    """Limpa todos os campos de entrada (Entry)."""
    for entry in entries:
        entry.delete(0, "end")

def preencher_campos(event, entries, tree):
    """Preenche os campos de entrada com os dados selecionados na árvore (treeview)."""
    selected = tree.selection()
    if selected:
        values = tree.item(selected, "values")
        for entry, val in zip(entries, values[1:]):  # pula o ID (primeira coluna)
            entry.delete(0, "end")
            entry.insert(0, val)

def validar_campos(marca, modelo, ano, preco):
    """Valida se todos os campos estão preenchidos e corretos."""
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
        messagebox.showwarning("Validação", "Preço deve ser um número decimal. (Ex: 19999.00)")
        return False

    return True

def formatar_preco(preco):
    """Formata o preço para o formato brasileiro: 1.999,99"""
    try:
        return f"{float(preco):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except ValueError:
        return preco


def vender_carro(carro):
    if carro:
        return carro
    else:
        return None

def validar_cpf(cpf):
    """Valida se o CPF possui exatamente 11 dígitos numéricos."""
    cpf = cpf.replace(".", "").replace("-", "").strip()  # Remove pontos, traços e espaços
    if cpf.isdigit() and len(cpf) == 11:
        return True
    else:
        return False
    
def capitalizar_texto(texto):
    """Capitaliza a primeira letra de cada palavra do texto."""
    return texto.capitalize()

def formatar_data_nascimento(texto):
    """Formata o texto para o formato DD/MM/AAAA enquanto digita."""
    apenas_digitos = ''.join(filter(str.isdigit, texto))[:8]
    
    if len(apenas_digitos) <= 2:
        return apenas_digitos
    elif len(apenas_digitos) <= 4:
        return f"{apenas_digitos[:2]}/{apenas_digitos[2:]}"
    else:
        return f"{apenas_digitos[:2]}/{apenas_digitos[2:4]}/{apenas_digitos[4:]}"
