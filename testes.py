
from core.security import  CRIPTO, verificar_senha, gerar_hash_senha, valida_cnpj, calcula_digito, eh_sequencia, apenas_numeros
import unittest


# Testes relacionados a senha.
class TestSenha(unittest.TestCase):

    # Teste da função que gera o hash das senha.
    def test_gerar_hash_senha(self):
        password = "senha12345"
        password_errado = "senha123"
        hash_password = gerar_hash_senha(password)

        # Teste para verificar se o hash ficou correto, senha usada válida.
        self.assertTrue(CRIPTO.verify(password, hash_password))

        # Teste para verificar se o hash ficou correto, senha usada inválida.
        self.assertFalse(CRIPTO.verify(password_errado, hash_password))


    # Teste da função que verifica se a senha esta correta através do hash.
    def test_verificar_senha(self):
        password = "senha12345"
        password_errado = "senha123"
        hash_password = gerar_hash_senha(password)

        # Teste a verificação da senha com senha válida.
        self.assertTrue(verificar_senha(password, hash_password))

        # Teste a verificação da senha com senha inválida.
        self.assertFalse(verificar_senha(password_errado, hash_password))


# Testes relacionados a CNPJ.
class TestCnpjFunctions(unittest.TestCase):

    # Função que testa se a validação de CNPJ está funcional.
    def test_valida_cnpj(self):
        cnpj = "34427619000107"
        cnpj_errado = "34427619999907"

        # Testa um CNPJ válido
        self.assertTrue(valida_cnpj(cnpj))

        # Testa um CNPJ inválido
        self.assertFalse(valida_cnpj(cnpj_errado))


    # Função que testa se a verificação de CNPJ sequencia está funcional.
    def test_eh_sequencia(self):
        cnpj = "34427619000107"
        cnpj_sequencia = "1111111111"

        # Testa um CNPJ que é sequência.
        self.assertFalse(eh_sequencia(cnpj))

        # Testa um CNPJ que não é sequência.
        self.assertTrue(eh_sequencia(cnpj_sequencia))


    # Função que testa se a transforação de CNPJ para apenas números está funcional.
    def test_apenas_numeros(self):
        cnpj_com_caracteres_invalidos = "61.577.705/0001-60"
        cnpj_sem_caracteres_invalidos = "61577705000160"

        # Testa a remoção de caracteres inválidos de um CNPJ.
        self.assertEqual(apenas_numeros(cnpj_com_caracteres_invalidos), cnpj_sem_caracteres_invalidos)

        # Testa a entrada sem caracteres inválidos de um CNPJ.
        self.assertEqual(apenas_numeros(cnpj_sem_caracteres_invalidos), cnpj_sem_caracteres_invalidos)


# Verificação se está sendo executado com o programa principal.
if __name__ == '__main__':
    unittest.main()
