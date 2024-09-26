# Gerador de CSV de Salários de Servidores

## Descrição

Este projeto consiste em um conjunto de scripts Python que utilizam a API do Portal da Transparência para gerar um arquivo CSV contendo os salários de todos os servidores da Universidade de Brasília (UnB). O projeto pode ser facilmente adaptado para outras instituições.

## Funcionalidades

- Obtém dados de servidores da API do Portal da Transparência
- Processa e organiza os dados dos servidores
- Coleta informações salariais dos últimos seis meses
- Gera um arquivo CSV com os dados coletados
- Realiza commit automático das alterações (requer configuração adicional)

## Requisitos

- Python 3.6+
- Bibliotecas: pandas, requests, python-dotenv
- Sistema operacional compatível com o comando `grep` (Linux, macOS, ou Windows com WSL)

## Considerações sobre o Sistema Operacional

Este projeto utiliza o comando `grep` em algumas partes do código, que é nativo em sistemas Unix (Linux e macOS). Para usuários do Windows, recomendamos as seguintes opções:

1. Usar o Windows Subsystem for Linux (WSL)
2. Instalar o Git Bash ou Cygwin, que fornecem uma versão do `grep`
3. Adaptar o código para usar alternativas em Python puro

## Como usar

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente no arquivo `.env`
4. Certifique-se de que o `grep` está disponível no seu sistema (veja as considerações acima)
5. Execute o script principal: `python gerar_csv.py`

## Estrutura do Projeto

- `funcionarios.py`: Define a classe Funcionario e funções para processar dados dos servidores
- `obter_servidores.py`: Obtém dados dos servidores da API
- `salarios.py`: Funções para obter e processar dados salariais
- `gerar_csv.py`: Script principal para gerar o arquivo CSV

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de submeter um pull request.
