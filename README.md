# Qualidade de Repositórios Java com GraphQL

## Descrição
Este projeto utiliza Python e a API GraphQL do GitHub para coletar e analisar métricas de qualidade de repositórios escritos em Java. O objetivo é extrair dados relevantes como data de criação, estrelas, forks, pull requests, issues abertas e releases, formatando-os para facilitar futuras análises.

## Requisitos
- Python 3.8 ou superior instalado.
- Token de acesso pessoal do GitHub (necessário para realizar requisições à API GraphQL).
- Arquivo `repositories.csv` com a lista de repositórios Java a serem analisados (já incluído no projeto).

## Instruções de Execução
1. Clone o repositório para sua máquina:
   ```bash
   git clone <URL-do-repositorio>
   cd java-repositories-quality-main
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o script principal:
   ```bash
   python code/main.py
   ```

## Saída
Os dados formatados serão salvos na pasta `outputs/`, com arquivos CSV contendo as informações detalhadas de cada repositório.

## Estrutura do Projeto
```
├── code/
│   ├── main.py               # Script principal de execução
│   ├── github_api.py         # Módulo para requisições à API do GitHub
│   ├── data_formatter.py     # Formatação e limpeza dos dados
│   └── query.gql             # Consulta GraphQL utilizada
├── outputs/                  # Resultados gerados pelo script
├── repositories.csv          # Lista de repositórios Java
└── requirements.txt          # Dependências do projeto
```

## Observações
- É recomendável não ultrapassar os limites de requisições da API do GitHub. O uso de um token evita bloqueios por excesso de requisições anônimas.
- Caso deseje analisar outros repositórios, adicione-os no arquivo `repositories.csv` no formato `usuario/repositorio`.
