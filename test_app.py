import unittest
import sqlite3
import os
from unittest.mock import patch
import utils
import database
import fipe_api

class TestUtils(unittest.TestCase):
    def test_validar_campos_validos(self):
        self.assertTrue(utils.validar_campos("Ford", "Ka", "2020", "25000"))

    def test_validar_campos_vazios(self):
        self.assertFalse(utils.validar_campos("", "Ka", "2020", "25000"))

    def test_validar_campos_ano_invalido(self):
        self.assertFalse(utils.validar_campos("Ford", "Ka", "ano", "25000"))

    def test_validar_campos_preco_invalido(self):
        self.assertFalse(utils.validar_campos("Ford", "Ka", "2020", "preco"))

    def test_formatar_preco_valido(self):
        self.assertEqual(utils.formatar_preco(19999.99), "19.999,99")

    def test_formatar_preco_invalido(self):
        self.assertEqual(utils.formatar_preco("abc"), "abc")

    def test_capitalizar_texto(self):
        self.assertEqual(utils.capitalizar_texto("joão da silva"), "João Da Silva")

    def test_validar_cpf_valido(self):
        self.assertTrue(utils.validar_cpf("12345678901"))

    def test_validar_cpf_invalido(self):
        self.assertFalse(utils.validar_cpf("123"))


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "teste_loja_carros.db"
        database.conectar_banco = lambda: sqlite3.connect(cls.db_name)
        database.criar_tabelas()

    def setUp(self):
        conn = sqlite3.connect(self.db_name, timeout=5)  # tenta esperar 5s se estiver travado
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carros")
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM historico")
        conn.commit()
        conn.close()


    def test_adicionar_e_listar_carro(self):
        database.adicionar_carro("Ford", "Ka", 2020, 25000, "ABC123456")
        carros = database.listar_carros()
        self.assertEqual(len(carros), 1)
        self.assertEqual(carros[0][1], "Ford")

    def test_editar_carro(self):
        database.adicionar_carro("Ford", "Ka", 2020, 25000, "ABC123456")
        carro_id = database.listar_carros()[0][0]
        database.editar_carro(carro_id, "Chevrolet", "Onix", 2022, 50000)
        carro = database.listar_carros()[0]
        self.assertEqual(carro[1], "Chevrolet")

    def test_remover_carro(self):
        database.adicionar_carro("Ford", "Ka", 2020, 25000, "ABC123456")
        carro_id = database.listar_carros()[0][0]
        database.remover_carro(carro_id)
        self.assertEqual(len(database.listar_carros()), 0)

    def test_registrar_e_autenticar_usuario(self):
        hash_fake = b"$2b$12$123456789012345678901u5DUJf8NoM3.7w5m7y/vAgC"
        sucesso, _ = database.registrar_usuario("usuario_teste", hash_fake, "123")
        self.assertTrue(sucesso)
        nivel = database.autenticar_usuario("usuario_teste")
        self.assertEqual(nivel[0], "VENDEDOR")

    def test_buscar_carro_por_id(self):
        database.adicionar_carro("Ford", "Ka", 2020, 25000, "ABC123456")
        carro_id = database.listar_carros()[0][0]
        carro = database.buscar_carro_por_id(carro_id)
        self.assertIsNotNone(carro)
        self.assertEqual(carro[1], "Ford")

    def test_inserir_e_validar_comprador(self):
        database.inserir_comprador("João Silva", "01/01/1990", "12345678901", "Rua A", "Apto 1", "Cliente")
        self.assertTrue(database.validar_comprador("12345678901"))
        dados = database.validar_dados_comprador("12345678901")
        self.assertEqual(dados[1], "João Silva")

    def test_registrar_venda(self):
        # Inserir vendedor e comprador
        conn = database.conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, hash_senha, nivel_acesso) VALUES (?, ?, ?)", ("vendedor", "hash", "VENDEDOR"))
        id_vendedor = cursor.lastrowid
        cursor.execute("INSERT INTO compradores (nome, data_nasc, cpf, endereco, complemento, cargo) VALUES (?, ?, ?, ?, ?, ?)",
                    ("João Silva", "01/01/2000", "12345678900", "Rua A", "", "Cliente"))
        id_comprador = cursor.lastrowid
        conn.commit()
        conn.close()

        # Registrar venda
        database.registrar_venda("Ford", "Ka", 2020, 25000, id_vendedor, "ABC123456", id_comprador)
        conn = database.conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historico")
        vendas = cursor.fetchall()
        conn.close()



    @classmethod
    def tearDownClass(cls):
        try:
            import gc
            gc.collect()  # força coleta de conexões
            if os.path.exists(cls.db_name):
                os.remove(cls.db_name)
        except Exception as e:
            print(f"Erro ao remover o banco de dados: {e}")



class TestFipeAPI(unittest.TestCase):
    @patch('fipe_api.requests.get')
    def test_listar_marcas(self, mock_get):
        mock_get.return_value.json.return_value = [{"nome": "Ford", "codigo": "1"}]
        marcas = fipe_api.listar_marcas()
        self.assertEqual(marcas[0]['nome'], "Ford")

    @patch('fipe_api.requests.get')
    def test_listar_modelos(self, mock_get):
        mock_get.return_value.json.return_value = {
            "modelos": [{"nome": "Ka", "codigo": "123"}]
        }
        modelos = fipe_api.listar_modelos("1")
        self.assertEqual(modelos[0]['nome'], "Ka")


if __name__ == "__main__":
    unittest.main()
