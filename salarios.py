import json
import time
import os
from datetime import datetime, timedelta
import calendar
import subprocess
import requests
import re
from funcionarios import UNIVERSIDADE
from obter_servidores import CHAVE_API
CUTOFF = 60
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores/remuneracao'

JSON_A_PRESERVAR = 'SERVIDORES_{UNIVERSIDADE}_TODOS.json'.format(UNIVERSIDADE = UNIVERSIDADE)


def apagar():
    comando = '''find . -type f -name '*.json' ! -name '{JSON_A_PRESERVAR}' -delete'''.format(JSON_A_PRESERVAR = JSON_A_PRESERVAR)
    subprocess.run(comando, shell=True)

def format_year_month(number):
    if 1 <= number <= 12:
        current_year = datetime.now().year
        if number < 10:
            return f"{current_year}0{number}"
        else:
            return f"{current_year}{number}"
    else:
        return "Number must be between 1 and 12."
    

def carrega_json(nome):
    with open(nome+'.json', 'r') as f:
        data = json.load(f)
    return data


def nomear_id(identificador):
    procurar_em = carrega_json(f'SERVIDORES_{UNIVERSIDADE}_TODOS')
    for elemento in procurar_em:
        if elemento['servidor']["idServidorAposentadoPensionista"] == identificador:
            return elemento['servidor']['pessoa']['nome']



def salva_json(resposta, nome):
    data=resposta.json()
    # Salvando o JSON em um arquivo
    if os.path.isfile(nome + '.json'):
        return  # Do nothing if the file already exists
    with open(nome+'.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def search_in_json(file_path, bruta):
    try:
        # Set pattern based on the value of bruta
        if bruta:
            pad = r'"remuneracaoBasicaBruta":\s*"\K[^"]*'
        else:
            pad = r'"valorTotalRemuneracaoAposDeducoes":\s*"\K[^"]*'
        
        # Using grep to find any value that matches the pattern
        result = subprocess.run(
            ['grep', '-oP', pad, file_path],
            capture_output=True, text=True
        )

        # Check if any matches were found and return the results
        if result.stdout:
            return result.stdout.strip().split('\n')
        else:
            return "Pattern not found." 
    except AssertionError:
        raise
    except Exception as e:
        return str(e)
def format_brl(value: float) -> str:
    """
    Converts a float number into Brazilian Real (BRL) format.
    
    Args:
        value (float): The float number to be converted.
        
    Returns:
        str: The formatted string in BRL (e.g., 'R$ 14.547,45').
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def busca_rem(arquivo, bruta):
    try:
        matches = search_in_json(arquivo, bruta)
        rem_string = matches[0]
        l = re.split(r'[,.]', rem_string)
        conv = l[0]+l[1] + '.' + l[2]
        return format_brl(float(conv))
    except IndexError:
        return 0
n_req = 1
COMEÇO = time.time()
total_time = 0
def pega_salario(ID_A_PROCURAR, mes):
    global url
    global n_req
    global COMEÇO
    NOME_A_SALVAR = nomear_id(ID_A_PROCURAR).replace(' ', '_') + '__' + mes + '___'+ f'REQUISICAO-{n_req}'
    elapsed_time = time.time() - COMEÇO
    # print(f'\n \n {int(total_time)} seconds past \n \n')
    n_req+=1
    print(NOME_A_SALVAR)
    print(f"\n Tempo passado: {elapsed_time:.2f} segundos \n")
    # assert elapsed_time <= CUTOFF, "TEMPO EXCEDIDO"
    # Definir os parâmetros da requisição
    params = {
        'id': ID_A_PROCURAR,
        'mesAno': mes,
        'pagina': 1
    }

    # Definir os headers da requisição
    headers = {
        'accept': '*/*',
        'chave-api-dados': CHAVE_API
    }

    # Fazer a requisição GET
    response = requests.get(url, headers=headers, params=params)


    salva_json(response, NOME_A_SALVAR)
    resultado = {"bruta": busca_rem(NOME_A_SALVAR + '.json', bruta=True), "liquida": busca_rem(NOME_A_SALVAR + '.json', bruta=False)}
    apagar()
    return resultado
    
    

def last_six_months():
    return ['202408']
    # # Get the current date
    # now = datetime.now()
    
    # # List to hold the last six months
    # months = []

    # # Loop to get the last six months
    # for i in range(1, 7):
    #     # Calculate the previous month
    #     previous_month = now.month - i
    #     previous_year = now.year
        
    #     # Adjust the year and month if the month goes below 1
    #     if previous_month <= 0:
    #         previous_month += 12
    #         previous_year -= 1
        
    #     # Format the month and year as YYYYMM
    #     formatted_month = f"{previous_year}{previous_month:02d}"
    #     months.append(formatted_month)
    
    # return months
if __name__ == '__main__':
    print(last_six_months())