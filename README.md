# Qualidade de Repositórios Java com GraphQL

## Descrição
Este projeto utiliza Python, a API GraphQL do GitHub e a ferramenta CK para coletar e analisar métricas de processo e de qualidade de repositórios escritos em Java. O objetivo é extrair dados relevantes como idade, estrelas, forks, releases, tamanho, CBO, DIT e LCOM.

## Métricas de Qualidade
Este projeto analisa as seguintes métricas de qualidade de software:

- **CBO (Coupling Between Objects - Acoplamento Entre Objetos)**: Mede o nível de dependência entre classes. Um CBO alto pode indicar um código fortemente acoplado, o que reduz a modularidade e dificulta a manutenção.
- **DIT (Depth of Inheritance Tree - Profundidade da Árvore de Herança)**: Representa a profundidade de uma classe na hierarquia de herança. Valores altos podem indicar maior complexidade e maior reutilização de código, mas também podem aumentar a dificuldade de compreensão e manutenção.
- **LCOM (Lack of Cohesion of Methods - Falta de Coesão dos Métodos)**: Mede a coesão dentro de uma classe. Um LCOM alto indica que a classe possui métodos que operam em subconjuntos diferentes dos atributos da classe, sugerindo que ela pode estar realizando múltiplas responsabilidades e pode precisar ser refatorada.
- **LOC (Lines of Code - Linhas de Código)**: Indica o tamanho do código-fonte em termos de linhas de código, sendo uma métrica geral usada para avaliar a complexidade e o esforço necessário para manutenção.

## Requisitos
- Python 3.8 ou superior instalado.
- Token de acesso pessoal do GitHub (necessário para realizar requisições à API GraphQL).
- Ferramenta CK configurada para ser utilizada na análise de métricas nos repositórios java.
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

3. Execute o script principal se quiser atualizar os 1000 repositórios java com mais estrelas. O novo arquivo repositories.csv será gerado dentro de outputs:
   ```bash
   python code/main.py
   ```

4. Execute o script de clonagem se quiser clonar repositórios para sua máquina. Você pode escolher quantos repositórios irá clonar depois de executar o comando abaixo:
   ```bash
   python code/clone_repos.py
   ```

5. Após coletar as métricas com CK, execute o script abaixo para sumarizar dados em uma planilha `summary_metrics` e atualizar `resultados.csv`.
   ```bash
   python code/calc_metrics.py
   ```

## Saída
- Os dados formatados serão salvos na pasta `outputs/`, com arquivos CSV contendo as informações detalhadas de cada repositório.
- Dentro de `outputs/ck/` estarão os dados coletados pela ferramenta CK e os resultados sumarizados pelo script `calc_metrics.py`.
- A planilha `repositories.csv` contém os dados coletados pela API do GitHub.
- A planilha final consolidada de resultados será salva em `docs/resultados.csv`, contendo as métricas do CK combinadas com os dados do GitHub.

## Observações
- É recomendável não ultrapassar os limites de requisições da API do GitHub. O uso de um token evita bloqueios por excesso de requisições anônimas.
- Certifique-se de rodar a ferramenta CK em cada repositório clonado antes de processar os dados com `calc_metrics.py`.
