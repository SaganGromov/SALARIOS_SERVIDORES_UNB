UNIVERSIDADE = "UNB"
DEPT_A_CHECAR="DEPTO MATEMATICA"


import json
import salarios
import pandas as pd


class Funcionario:
    def __init__(self, idServidorAposentadoPensionista, situacao, nome, dept):
        self.idServidorAposentadoPensionista = idServidorAposentadoPensionista
        self.situacao = situacao
        self.nome = nome
        self.dept = dept
        self.salarios = {}  # Dicionário para armazenar salários por mês

    def definir_salario(self, mes, salario):
        """Define o salário de um determinado mês."""
        self.salarios[mes] = salario

    def obter_salario(self, mes):
        """Retorna o salário de um determinado mês, ou None se não houver salário definido."""
        return self.salarios.get(mes, None)
    
    def listar_atributos(self):
        """Itera e imprime todos os atributos e seus valores"""
        for atributo, valor in self.__dict__.items():
            print(f"{atributo}: {valor}")
    def teste(self):
        print("teste")



with open(f"SERVIDORES_{UNIVERSIDADE}_TODOS.json", 'r') as file:
    # Load the JSON content into a list
    SERVIDORES = json.load(file)
# Criando um funcionário
c = 0
SERVIDORES_TRATADOS = []
NAO_TESTAR_TODOS = True
LIMITE_DE_TESTE = 10**10
for elemento in SERVIDORES:
    try:
        servidor = elemento['servidor']
        dept = elemento['fichasCargoEfetivo'][0]["uorgExercicio"]
        # if dept in DEPT_A_CHECAR:
        funcionario = Funcionario(idServidorAposentadoPensionista=servidor['idServidorAposentadoPensionista'], situacao = servidor['situacao'], nome = servidor['pessoa']['nome'], dept = elemento['fichasCargoEfetivo'][0]["uorgExercicio"])
        # funcionario.listar_atributos()
        SERVIDORES_TRATADOS.append({"idServidorAposentadoPensionista": servidor['idServidorAposentadoPensionista'], "situacao": servidor['situacao'], "nome": servidor['pessoa']['nome'], "dept": elemento['fichasCargoEfetivo'][0]["uorgExercicio"], "salarios": {}})
    except AssertionError:
        raise
    except Exception as e:
        pass
    if NAO_TESTAR_TODOS:
        c += 1
        if c == LIMITE_DE_TESTE:
            break
nc = 0
for servidor in SERVIDORES_TRATADOS:
    try:
        for i in salarios.last_six_months():
            dept = servidor['dept']
            ID = servidor['idServidorAposentadoPensionista']
            sal = salarios.pega_salario(ID_A_PROCURAR=ID, mes = i)
            bruta = sal['bruta']
            liquida = sal['liquida']
            servidor['salarios'][i] = {"REMUNERACAO BRUTA": bruta, "REMUNERACAO LIQUIDA": liquida}
    except AssertionError:
        raise
    except Exception as e:
        # teste pra commitar sep23 at23h53
        print(e)
        pass 
    if NAO_TESTAR_TODOS:
        nc += 1
        if nc == LIMITE_DE_TESTE:
            break
print('\n \n')
# for servidor in SERVIDORES_TRATADOS:
#     print(servidor)
#     print('\n \n')