import json
import time
import os
from datetime import datetime
import subprocess
import requests
import re
from funcionarios import UNIVERSIDADE
from obter_servidores import CHAVE_API

CUTOFF = 60
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/remuneracao'

JSON_A_PRESERVAR = f'SERVIDORES_{UNIVERSIDADE}_TODOS.json'

def apagar():
    """Apaga todos os arquivos JSON exceto o especificado em JSON_A_PRESERVAR."""
    comando = f'''find . -type f -name '*.json' ! -name '{JSON_A_PRESERVAR}' -delete'''
    subprocess.run(comando, shell=True)

def carrega_json(nome):
    """Carrega um arquivo JSON e retorna seu conteúdo."""
    with open(nome+'.json', 'r') as f:
        return json.load(f)

def nomear_id(identificador):
    """Retorna o nome do servidor com base no seu identificador."""
    procurar_em = carrega_json(f'SERVIDORES_{UNIVERSIDADE}_TODOS')
    for elemento in procurar_em:
        if elemento['servidor']["idServidorAposentadoPensionista"] == identificador:
            return elemento['servidor']['pessoa']['nome']
    return "Nome não encontrado"

def salva_json(resposta, nome):
    """Salva a resposta da API em um arquivo JSON se ele não existir."""
    if not os.path.isfile(nome + '.json'):
        with open(nome+'.json', 'w') as f:
            json.dump(resposta.json(), f, indent=4, sort_keys=True, ensure_ascii=False)

def search_in_json(file_path, bruta):
    """Busca um padrão específico no arquivo JSON."""
    try:
        pad = r'"remuneracaoBasicaBruta":\s*"\K[^"]*' if bruta else r'"valorTotalRemuneracaoAposDeducoes":\s*"\K[^"]*'
        result = subprocess.run(['grep', '-oP', pad, file_path], capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout else "Padrão não encontrado."
    except Exception as e:
        return str(e)

def format_brl(value: float) -> str:
    """Formata um número float para o formato de moeda brasileira (BRL)."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def busca_rem(arquivo, bruta):
    """Busca e formata a remuneração no arquivo JSON."""
    try:
        matches = search_in_json(arquivo, bruta)
        rem_string = matches[0]
        l = re.split(r'[,.]', rem_string)
        conv = l[0]+l[1] + '.' + l[2]
        return format_brl(float(conv))
    except IndexError:
        return "R$ 0,00"

n_req = 1
COMEÇO = time.time()

def pega_salario(ID_A_PROCURAR, mes):
    """Obtém o salário de um servidor para um determinado mês."""
    global n_req, COMEÇO
    NOME_A_SALVAR = nomear_id(ID_A_PROCURAR).replace(' ', '_') + '__' + mes + '___'+ f'REQUISICAO-{n_req}'
    elapsed_time = time.time() - COMEÇO
    n_req += 1
    print(NOME_A_SALVAR)
    print(f"\n Tempo passado: {elapsed_time:.2f} segundos \n")

    params = {
        'id': ID_A_PROCURAR,
        'mesAno': mes,
        'pagina': 1
    }
    headers = {
        'accept': '*/*',
        'chave-api-dados': CHAVE_API
    }

    response = requests.get(url, headers=headers, params=params)
    salva_json(response, NOME_A_SALVAR)
    resultado = {"bruta": busca_rem(NOME_A_SALVAR + '.json', bruta=True), 
                 "liquida": busca_rem(NOME_A_SALVAR + '.json', bruta=False)}
    apagar()
    return resultado

def last_six_months():
    """Retorna uma lista com os últimos seis meses no formato YYYYMM."""
    return ['202408']  # Temporariamente retornando apenas um mês para teste

if __name__ == '__main__':
    print(last_six_months())