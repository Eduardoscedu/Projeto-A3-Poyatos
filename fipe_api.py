# fipe_api.py
import requests

def listar_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    return requests.get(url).json()

def listar_modelos(marca_codigo):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{marca_codigo}/modelos"
    return requests.get(url).json()['modelos']
