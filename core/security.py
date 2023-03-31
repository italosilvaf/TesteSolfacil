from passlib.context import CryptContext
import re

# Configuração do algoritmo e força de criptografia.
CRIPTO = CryptContext(schemes=['bcrypt'],
                      deprecated='auto',  bcrypt__rounds=10)


# Função de erificação de senha, onde verifica se a senha é conpatível com o hash salvo no banco de dados.
def verificar_senha(password: str, hash_password: str) -> bool:
    return CRIPTO.verify(password, hash_password)


# Função para gerar o hash de uma senha.
def gerar_hash_senha(password: str) -> str:
    return CRIPTO.hash(password)


# Função para validar cnpj.
def valida_cnpj(cnpj):
    cnpj = apenas_numeros(cnpj)

    try:
        if eh_sequencia(cnpj):
            return False
    except:
        return False
    
    try:
        novo_cnpj = calcula_digito(cnpj=cnpj, digito=1)
        novo_cnpj = calcula_digito(cnpj=novo_cnpj, digito=2)
    except Exception as e:
        return False

    if novo_cnpj == cnpj:
        return True
    else:
        return False


# Função para calcular cada um dos dois dígitos verificadores do CNPJ
def calcula_digito(cnpj, digito):
    REGRESSIVOS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    if digito == 1:
        regressivos = REGRESSIVOS[1:]
        novo_cnpj = cnpj[:-2]
    elif digito == 2:
        regressivos = REGRESSIVOS
        novo_cnpj = cnpj
    else:
        return None

    total = 0

    for indice, regressivo in enumerate(regressivos):
        total += int(cnpj[indice]) * regressivo

    digito = 11 - (total % 11)
    digito = digito if digito <= 9 else 0

    return f'{novo_cnpj}{digito}'


# Função verifica se o CNPJ é uma sequência de dígitos repetidos.
def eh_sequencia(cnpj):
    sequencia = cnpj[0] * len(cnpj)

    if sequencia == cnpj:
        return True
    else:
        return False

# Função para remover qualquer caractere que não seja um número.
def apenas_numeros(x):
    return re.sub(r'[^0-9]', '', x)


# Função para verifica se o CEP contém apenas números
def verifica_apenas_numeros(cep):
    if re.match(r'^\d+$', cep):
        return True
    else:
        return False