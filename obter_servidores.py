import requests
import json
import os
from funcionarios import UNIVERSIDADE
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()
CHAVE_API = os.getenv('CHAVE_API')

# Define a URL base e os headers
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores'
headers = {
    'accept': '*/*',
    'chave-api-dados': CHAVE_API
}

# Inicializa o número da página
page = 1
all_data = []

while True:
    # Define os parâmetros de consulta para a página atual
    params = {
        'tipoServidor': 1,
        'situacaoServidor': 1,
        'orgaoServidorLotacao': 26239,
        'pagina': page
    }

    # Faz a requisição GET
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    # Para se a resposta for uma lista vazia
    if not response_data:
        print(f"Resposta vazia na página {page}. Parando.")
        break

    # Define o nome do arquivo e salva os dados da resposta em um arquivo JSON
    filename = f'SERVIDORES_{UNIVERSIDADE}_PAGINA_{page}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=4, ensure_ascii=False)
    
    print(f"Dados da página {page} salvos em {filename}")
    
    # Adiciona os dados à lista all_data
    all_data.extend(response_data)

    # Incrementa o número da página para a próxima requisição
    page += 1

# Salva todos os dados concatenados em um único arquivo JSON
with open(f'SERVIDORES_{UNIVERSIDADE}_TODOS.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"Todas as páginas concatenadas em SERVIDORES_{UNIVERSIDADE}_TODOS.json")
