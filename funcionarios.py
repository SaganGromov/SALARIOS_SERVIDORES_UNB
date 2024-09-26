UNIVERSIDADE = "UNB"
DEPT_A_CHECAR="DEPTO MATEMATICA"


import json
import salarios
import pandas as pd
from typing import Dict, Any, List


class Funcionario:
    def __init__(self, idServidorAposentadoPensionista: str, situacao: str, nome: str, dept: str):
        self.idServidorAposentadoPensionista = idServidorAposentadoPensionista
        self.situacao = situacao
        self.nome = nome
        self.dept = dept
        self.salarios: Dict[str, Dict[str, float]] = {}

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Funcionario object to a dictionary."""
        return {
            "idServidorAposentadoPensionista": self.idServidorAposentadoPensionista,
            "situacao": self.situacao,
            "nome": self.nome,
            "dept": self.dept,
            "salarios": self.salarios
        }


def process_servidores(servidores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    servidores_tratados = []
    for elemento in servidores:
        try:
            servidor = elemento['servidor']
            dept = elemento['fichasCargoEfetivo'][0]["uorgExercicio"]
            funcionario = Funcionario(
                idServidorAposentadoPensionista=servidor['idServidorAposentadoPensionista'],
                situacao=servidor['situacao'],
                nome=servidor['pessoa']['nome'],
                dept=dept
            )
            servidores_tratados.append(funcionario.to_dict())
        except Exception as e:
            print(f"Error processing servidor: {e}")
    
    return servidores_tratados

def add_salarios(servidores_tratados: List[Dict[str, Any]]) -> None:
    for servidor in servidores_tratados:
        try:
            for mes in salarios.last_six_months():
                sal = salarios.pega_salario(ID_A_PROCURAR=servidor['idServidorAposentadoPensionista'], mes=mes)
                servidor['salarios'][mes] = {"REMUNERACAO BRUTA": sal['bruta'], "REMUNERACAO LIQUIDA": sal['liquida']}
        except Exception as e:
            print(f"Error adding salarios for servidor {servidor['idServidorAposentadoPensionista']}: {e}")

if __name__ == "__main__":
    with open(f"SERVIDORES_{UNIVERSIDADE}_TODOS.json", 'r') as file:
        SERVIDORES = json.load(file)
    
    servidores_tratados = process_servidores(SERVIDORES)
    add_salarios(servidores_tratados)

    # Uncomment to print results
    # for servidor in servidores_tratados:
    #     print(servidor)
    #     print('\n \n')