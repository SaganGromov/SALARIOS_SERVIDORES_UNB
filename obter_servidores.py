import requests
import json
import os
from funcionarios import UNIVERSIDADE
from dotenv import load_dotenv
load_dotenv()
CHAVE_API = os.getenv('CHAVE_API')



# Define the base URL and headers
url = 'https://api.portaldatransparencia.gov.br/api-de-dados/servidores'
headers = {
    'accept': '*/*',
    'chave-api-dados': CHAVE_API
}

# Initialize the page number
page = 1
all_data = []

while True:
    # Define query parameters for the current page
    params = {
        'tipoServidor': 1,
        'situacaoServidor': 1,
        'orgaoServidorLotacao': 26239,
        'pagina': page
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    # Stop if the response data is an empty list
    if response_data == []:
        print(f"Empty response at page {page}. Stopping.")
        break

    # Define the filename and save the response data to a JSON file
    filename = f'SERVIDORES_{UNIVERSIDADE}_PAGINA_{page}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=4, ensure_ascii=False)  # Human-readable format
    
    print(f"Saved page {page} data to {filename}")
    
    # Append the data to the all_data list
    all_data.extend(response_data)

    # Increment the page number for the next request
    page += 1

# Save all the concatenated data into a single JSON file
with open(f'SERVIDORES_{UNIVERSIDADE}_TODOS.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)  # Human-readable format

print(f"All pages concatenated into SERVIDORES_{UNIVERSIDADE}_TODOS.json")
