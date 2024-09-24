import pandas as pd
from funcionarios import SERVIDORES_TRATADOS    
from funcionarios import UNIVERSIDADE
import time
import subprocess
data = SERVIDORES_TRATADOS
NOME_CSV = 'SALARIO_SERVIDORES_{UNIVERSIDADE}_AGOSTO_COMMIT_AUTOMATIZADO'.format(UNIVERSIDADE=UNIVERSIDADE)
# List to store the flattened data
rows = []

# Extract the relevant data
for person in data:
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

# Create a DataFrame


df = pd.DataFrame(rows).sort_values(by='NOME')
df.to_csv(NOME_CSV, index = False)

print("\n CSV gerado! \n")
comando="zsh -i -c 'vai'"
subprocess.run(comando, shell=True)
print("\n \n Commit subiu! \n \n")