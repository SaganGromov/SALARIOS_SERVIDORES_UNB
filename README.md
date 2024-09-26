# Gerador de CSV de Salários de Servidores

## Descrição

Este projeto consiste em um conjunto de scripts Python que utilizam a API do Portal da Transparência para gerar um arquivo CSV contendo os salários de todos os servidores da Universidade de Brasília (UnB). O projeto pode ser facilmente adaptado para outras instituições.

## API do Portal da Transparência

Este projeto utiliza a API do Portal da Transparência do Governo Federal. A documentação completa da API pode ser encontrada em:

[https://api.portaldatransparencia.gov.br/swagger-ui/index.html](https://api.portaldatransparencia.gov.br/swagger-ui/index.html)

## Funcionalidades

- Obtém dados de servidores da API do Portal da Transparência
- Processa e organiza os dados dos servidores
- Coleta informações salariais dos últimos seis meses
- Gera um arquivo CSV com os dados coletados
- Realiza commit automático das alterações (requer configuração adicional, veja [commit-preguicoso](https://github.com/SaganGromov/commit-preguicoso))

## Requisitos

- Python 3.6+
- Bibliotecas: pandas, requests, python-dotenv
- Sistema operacional compatível com o comando `grep` (Linux, macOS, ou Windows com WSL)
- Token de acesso à API do Portal da Transparência

## Considerações sobre o Sistema Operacional

Este projeto utiliza o comando `grep` em algumas partes do código, que é nativo em sistemas Unix (Linux e macOS). Para usuários do Windows, recomendamos as seguintes opções:

1. Usar o Windows Subsystem for Linux (WSL)
2. Instalar o Git Bash ou Cygwin, que fornecem uma versão do `grep`
3. Adaptar o código para usar alternativas em Python puro

## Como usar

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` no diretório raiz do projeto
4. Adicione seu token de acesso à API no arquivo `.env`:
   ```
   CHAVE_API='<seu_token_aqui>'
   ```
5. Certifique-se de que o `grep` está disponível no seu sistema (veja as considerações acima)
6. Execute o script principal: `python3 gerar_csv.py`

## Estrutura do Projeto

- `funcionarios.py`: Define a classe Funcionario e funções para processar dados dos servidores
- `obter_servidores.py`: Obtém dados dos servidores da API
- `salarios.py`: Funções para obter e processar dados salariais
- `gerar_csv.py`: Script principal para gerar o arquivo CSV

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de submeter um pull request.
