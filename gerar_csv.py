import pandas as pd
from funcionarios import process_servidores, add_salarios
from funcionarios import UNIVERSIDADE
import json
import subprocess

# Carrega os dados dos servidores
with open(f"SERVIDORES_{UNIVERSIDADE}_TODOS.json", 'r') as file:
    SERVIDORES = json.load(file)

# Processa os servidores e adiciona os salários
servidores_tratados = process_servidores(SERVIDORES)
add_salarios(servidores_tratados)

NOME_CSV = f'SALARIO_SERVIDORES_{UNIVERSIDADE}_AGOSTO_COMMIT_AUTOMATIZADO.csv'

# Lista para armazenar os dados planificados
rows = []

# Extrai os dados relevantes
for person in servidores_tratados:
    nome = person['nome']
    situacao = person['situacao']
    id_servidor = person['idServidorAposentadoPensionista']
    dept = person['dept']
    for mes, salarios in person['salarios'].items():
        bruto = salarios.get('REMUNERACAO BRUTA', 'N/A')
        liquido = salarios.get('REMUNERACAO LIQUIDA', 'N/A')
        rows.append({
            'NOME': nome,
            'ID': id_servidor,
            'SITUACAO': situacao,
            'DEPARTAMENTO': dept,
            'MES': mes,
            'REMUNERACAO BRUTA': bruto,
            'REMUNERACAO LIQUIDA': liquido
        })

# Cria um DataFrame e ordena por nome
df = pd.DataFrame(rows).sort_values(by='NOME')

# Salva o DataFrame como CSV
df.to_csv(NOME_CSV, index=False)

print("\n CSV gerado! \n")

# Executa o comando de commit (assumindo que 'vai' é um alias para o comando git)
comando = "zsh -i -c 'vai'"
subprocess.run(comando, shell=True)

print("\n \n Commit subiu! \n \n")