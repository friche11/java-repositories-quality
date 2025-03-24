# Relatório Final

## Introdução

Neste estudo, analisamos os 1.000 repositórios desenvolvidos na linguagem java mais populares do GitHub, considerando o número de estrelas como critério de popularidade. O objetivo é analisar aspectos da qualidade desses repositórios, correlacionando-os com características como popularidade, tamanho, atividade e maturidade. As métricas de qualidade foram calculadas utilizando a ferramenta **CK**.

## Hipóteses Iniciais

#### RQ 01. Qual a relação entre a popularidade dos repositórios e suas características de qualidade?
  _É provável que repositórios populares em java tendem a ter melhor qualidade, com menor acoplamento (CBO) e maior coesão (LCOM), pois boas práticas de design são mais comuns em projetos amplamente adotados. No entanto, podem ter hierarquias de herança mais profundas (DIT) devido à evolução do código._

#### RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
  _É provável que repositórios mais antigos em java podem apresentar maior complexidade, com aumento no acoplamento (CBO) e menor coesão (LCOM), pois o código evolui ao longo do tempo. Além disso, podem desenvolver hierarquias de herança mais profundas (DIT) à medida que o código cresce._

#### RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
  _É provável que repositórios mais ativos tendem a ter menor acoplamento (CBO) e maior coesão (LCOM), pois a manutenção frequente melhora a estrutura do código. É possível também que a atividade dos repositórios aumenta as hierarquias de herança (DIT), já que um número maior de releases indica que o código cresceu ao ponto de novas versões serem lançadas._

#### RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
  _É provável que repositórios maiores podem ter maior acoplamento (CBO) e menor coesão (LCOM), pois a complexidade cresce com o número de classes e métodos. Além disso, a profundidade da herança (DIT) pode aumentar conforme novas camadas de abstração são introduzidas._
  
## Metodologia

Para responder às questões de pesquisa, realizamos a coleta e análise de dados dos 1.000 repositórios Java mais populares no GitHub, seguindo os seguintes passos:
1. **Coleta de Dados dos Repositórios:**  
   - Executamos um script principal `main.py` que utiliza a API GraphQL do GitHub para buscar os repositórios com maior número de estrelas.  
   - Os dados extraídos incluem nome, autor, número de estrelas, data de criação (para calcular a maturidade), número de forks e número de releases.
   - Os resultados foram armazenados em um arquivo `repositories.csv` dentro da pasta `outputs`.
  
   - Depois de ter a planilha com os repositórios, executamos o script `clone_repos.py`, que percorre a planilha de repositórios e clona cada um pelo nome identificado na pasta `repositories`
   - Executamos o script `calc_metrics.py` escolhendo a opção 1 para executar a ferramenta CK em cada repositório clonado, gerando as planilhas que contêm dados sobre as métricas de qualidade dentro das pastas `outputs/ck`. No final da execução é gerado uma nova planilha para cada repositório com dados sumarizados pela média, mediana e desvio padrão para CBO, DIT, LCOM E LOC.
   - As métricas extraídas e analisadas foram:
     - **CBO (Acoplamento Entre Objetos):** Mede a dependência entre classes. Valores altos indicam forte acoplamento, dificultando manutenção e reutilização.  
     - **DIT (Profundidade da Árvore de Herança):** Representa a profundidade máxima da hierarquia de herança. Um DIT alto pode indicar maior reutilização de código, mas também maior complexidade.  
     - **LCOM (Falta de Coesão dos Métodos):** Mede a independência entre os métodos de uma classe. Valores altos indicam baixa coesão, prejudicando modularidade e manutenção.  
     - **LOC (Linhas de Código):** Mede o tamanho do código-fonte.
     
2. **Análise de Dados dos Repositórios:**
   - Ao executar a opção 2 do script `calc_metrics.py` a planilha `repositories.csv` e essas novas planilhas sumarizadas dos dados de qualidade individuais de cada repositório foram unificadas em uma planilha de `resultados.csv` dentro da pasta `docs`
   - Executamos novamente o script `calc_metrics.py` na opção 3 para analisar os dados com estatística descritiva: Os repositórios foram agrupados com base na mediana das métricas gerais para comparação com as métricas de qualidade. Os dados gerados estão na planilha `analise_resultados.csv` na pasta `docs`.
   - Executamos também o script `calc_metrics.py` na opcão 4 para analisar os dados pelo teste estatístico de Spearman para verificar a análise anterior. Os dados foram salvos em `analise_correlacao_spearman.csv` na pasta `docs`.

## Resultados Obtidos

### RQ01: Qual a relação entre a popularidade dos repositórios e suas características de qualidade?

**Gráfico CBO x Popularidade**

![image](https://github.com/user-attachments/assets/8a841deb-d1e3-4840-a862-eea359e3e280)

**Gráfico DIT x Popularidade**

![image](https://github.com/user-attachments/assets/354e2551-bab4-4ceb-a5e3-80b68154ec7d)

**Gráfico LCOM x Popularidade**

![image](https://github.com/user-attachments/assets/5aaa399a-db5c-44b7-bd1d-d85c4dbc76fc)

**Gráfico LOC x Popularidade**

![image](https://github.com/user-attachments/assets/d3c7154b-c93a-49f3-b808-7700846b176d)

A análise da relação entre Popularidade (Estrelas) e métricas de qualidade mostra que:

- **LCOM** é a métrica que apresenta diferença relevante entre repositórios populares e não populares.
  - Média: **455.91 (Alto)** vs. **299.27 (Baixo)**.
  - Mediana: **19.38 (Alto)** vs. **15.81 (Baixo)**.
  - Desvio Padrão: **5077.42 (Alto)** vs. **2477.47 (Baixo)**.
- **CBO**, **DIT**, e **LOC** não apresentam diferenças significativas entre os grupos analisados.

A análise sugere que repositórios populares tendem a apresentar maior Falta de Coesão dos Métodos (**LCOM**), indicando possíveis problemas relacionados à coesão do código.

### RQ02: Qual a relação entre a maturidade dos repositórios e suas características de qualidade?

**Gráfico CBO x Maturidade**

![image](https://github.com/user-attachments/assets/d602505c-8c6c-40d0-bf93-b10060f1d9bd)

**Gráfico DIT x Maturidade**

![image](https://github.com/user-attachments/assets/4382f04f-c869-4b4f-a222-c0e23e35c200)

**Gráfico LCOM x Maturidade**

![image](https://github.com/user-attachments/assets/7208a009-0ad2-47f3-8d83-4e51778fb8a9)

**Gráfico LOC x Maturidade**

![image](https://github.com/user-attachments/assets/fc651d7b-a871-42fa-b860-2e7539577d78)

A análise da relação entre Maturidade (Anos) e métricas de qualidade mostra que:

- **LCOM** apresenta diferença significativa no desvio padrão, indicando maior variação na coesão do código em repositórios mais antigos.

  - Média: **850.0 (Alto)** vs. **620.0 (Baixo)**.
  - Mediana: **800.0 (Alto)** vs. **600.0 (Baixo)**.
  - Desvio Padrão: **110.0 (Alto)** vs. **85.0 (Baixo)**.

- As métricas **LOC, DIT** e **CBO** não apresentam diferenças relevantes entre os grupos analisados.

A análise sugere que, embora repositórios mais antigos possuam uma variação maior de coesão do código (**LCOM**), isso pode indicar diferenças no estilo de programação ou na evolução do projeto ao longo do tempo.

### RQ03: Qual a relação entre a atividade dos repositórios e suas características de qualidade?

**Gráfico CBO x Atividade**

![image](https://github.com/user-attachments/assets/615253d3-79b3-42cc-a8d5-b4d5054fbe5a)

**Gráfico DIT x Atividade**

![image](https://github.com/user-attachments/assets/f47b1c00-b847-44d8-a8bb-4664a9d503e7)

**Gráfico LCOM x Atividade**

![image](https://github.com/user-attachments/assets/02f1bad4-4f9b-4feb-a6dc-f1ebe783ab7a)

**Gráfico LOC x Atividade**

![image](https://github.com/user-attachments/assets/01614365-a1f2-4871-9caa-ba4f642447ce)

A análise da relação entre Atividade (Número de Releases) e métricas de qualidade mostra que:

- **DIT** apresenta uma variação significativa no Desvio Padrão, sugerindo que repositórios mais ativos possuem uma hierarquia de herança mais diversificada.

  - Média: **1.21 (Alto)** vs. **1.18 (Baixo)**.
  - Mediana: **1.00 (Alto)** vs. **1.00 (Baixo)**.
  - Desvio Padrão: **0.17 (Alto)** vs. **0.13 (Baixo)**.

- **LCOM** mostra diferenças importantes na Média e no Desvio Padrão, sugerindo que repositórios mais ativos têm menor coesão.

  - Média: **450.36 (Alto)** vs. **293.25 (Baixo)**.
  - Mediana: **24.78 (Alto)** vs. **11.32 (Baixo)**.
  - Desvio Padrão: **4904.42 (Alto)** vs. **2558.82 (Baixo)**.

- A métrica **CBO** não apresenta diferenças significativas.

A análise sugere que a atividade dos repositórios influencia negativamente a coesão do código (**LCOM**) e gera maior diversidade na hierarquia de herança (**DIT**), o que pode indicar complexidade adicional na estrutura do código.

### RQ04: Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

**Gráfico CBO x Tamanho**

![image](https://github.com/user-attachments/assets/383885fe-ff7b-403f-9303-370bf8ea51f3)

**Gráfico DIT x Tamanho**

![image](https://github.com/user-attachments/assets/3a15dc68-f2cb-4ec1-bdb2-9a3f8ccf1b47)

**Gráfico LCOM x Tamanho**
![image](https://github.com/user-attachments/assets/5120e5af-4e5d-4df2-baa6-0bc12f593ac4)

**Gráfico LOC x Tamanho**

![image](https://github.com/user-attachments/assets/caa296bb-3ed1-418b-8303-6da7f812e0a7)

A análise da relação entre Tamanho (Linhas de Código - LOC) e métricas de qualidade mostra que:

- **CBO** apresenta valores significativamente mais altos em repositórios maiores, sugerindo maior acoplamento entre classes.

  - Média: **3.14 (Alto)** vs. **1.88 (Baixo)**.
  - Mediana: **3.01 (Alto)** vs. **2.00 (Baixo)**.
  - Desvio Padrão: **1.07 (Alto)** vs. **0.84 (Baixo)**.

- **DIT** possui uma variação perceptível no Desvio Padrão, indicando uma possível hierarquia de herança mais diversificada em projetos maiores.

  - Desvio Padrão: **0.19 (Alto)** vs. **0.15 (Baixo)**.

- **LCOM** apresenta diferenças extremamente relevantes, indicando menor coesão em projetos maiores.

  - Média: **729.64 (Alto)** vs. **22.03 (Baixo)**.
  - Mediana: **80.53 (Alto)** vs. **1.00 (Baixo)**.
  - Desvio Padrão: **5598.70 (Alto)** vs. **151.22 (Baixo)**.

- **LOC** é uma métrica básica que mostra claramente que repositórios maiores têm código consideravelmente mais extenso.

  - Média: **1150.0 (Alto)** vs. **870.0 (Baixo)**.
  - Mediana: **970.0 (Alto)** vs. **770.0 (Baixo)**.
  - Desvio Padrão: **170.0 (Alto)** vs. **135.0 (Baixo)**.

## Resultados com teste estatístico de Spearman

**Matriz de Correlação de Spearman**

![image](https://github.com/user-attachments/assets/7c4f30a5-4d93-499b-86c3-0f6d55ea59a4)

A matriz apresenta correlações entre Popularidade, Maturidade, Atividade e Tamanho com as métricas de qualidade (CBO, DIT, LCOM, LOC). A correlação varia de -1 a 1:

- Valores próximos de 1: Forte correlação positiva (quando uma variável aumenta, a outra também tende a aumentar).

- Valores próximos de -1: Forte correlação negativa (quando uma variável aumenta, a outra tende a diminuir).

- Valores próximos de 0: Sem correlação significativa.

#### RQ 01. Qual a relação entre a popularidade dos repositórios e suas características de qualidade?
- Não há correlação significativa entre Estrelas e métricas de qualidade como CBO, DIT, LCOM ou LOC. A correlação mais alta é com LCOM (0.02), que é praticamente nula.

- O número de estrelas não influencia diretamente as características de qualidade dos repositórios.

#### RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
- Maturidade tem uma correlação positiva fraca com DIT (0.16), indicando que repositórios mais antigos têm levemente mais profundidade de herança.

- Há uma pequena correlação com LCOM (0.12), sugerindo que repositórios mais antigos podem ter menor coesão.

- A maturidade dos repositórios parece influenciar apenas levemente a profundidade da herança e a coesão do código.

#### RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- As releases mostram uma correlação positiva fraca com CBO (0.20), sugerindo que repositórios mais ativos podem ter maior acoplamento.

- Correlação muito fraca com LCOM (0.12) e LOC (0.05), o que sugere que a atividade não impacta significativamente a coesão ou o tamanho do código.

- Repositórios mais ativos podem apresentar maior acoplamento, mas a relação com outras métricas de qualidade é quase inexistente.

#### RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
- As linhas de código mostram uma correlação alta com CBO (0.71), LCOM (0.85), indicando que projetos maiores têm maior acoplamento e menor coesão.

- A correlação com DIT (-0.01) é praticamente nula, indicando que o tamanho do código não afeta a profundidade da herança.

- Projetos maiores apresentam significativamente mais acoplamento entre objetos e menor coesão dos métodos.
- 
## Analisando os gráficos obtidos e a Matriz de Correlação de Spearman:

- A matriz de Spearman confirmou que o **Tamanho dos Repositórios (LOC)** é a principal variável que influencia negativamente a qualidade do código, com correlações altas para **CBO (0.71)** e **LCOM (0.85)**. Esse resultado está alinhado com os gráficos que mostram o aumento de **CBO e LCOM** para repositórios maiores.

- A **Popularidade (Estrelas)** não mostrou correlações relevantes com as métricas de qualidade, indicando que o sucesso de um repositório em termos de estrelas não garante qualidade interna. Isso é confirmado tanto pela matriz quanto pelos gráficos.

- A **Maturidade (Anos)** apresentou correlação positiva fraca com **DIT (0.16)** e leve correlação com **LCOM (0.12)**, sugerindo que repositórios mais antigos têm maior profundidade de herança e menor coesão do código. Essa relação é compatível com os gráficos gerados, embora o impacto seja pequeno.

- A **Atividade (Releases)** apresentou uma leve correlação com **CBO (0.20)**, indicando que repositórios mais ativos tendem a ter um maior acoplamento entre objetos. Contudo, a influência sobre **LCOM e LOC** é praticamente nula, o que é consistente com os resultados visuais dos gráficos.

De forma geral, a matriz de Spearman valida os resultados obtidos nos gráficos para cada uma das RQs, mostrando que as métricas **CBO e LCOM** são as mais afetadas por variáveis como **Tamanho** e, em menor grau, **Atividade e Maturidade**.


## Conclusão

Os resultados mostram que **Popularidade, Maturidade, Atividade e Tamanho** dos repositórios afetam principalmente as métricas **CBO** e **LCOM**, indicando maior acoplamento e menor coesão. **DIT** não apresenta alterações significativas com relação a essas variáveis.  
O estudo demonstrou que repositórios maiores apresentam maior acoplamento e menor coesão, o que pode indicar dificuldades na manutenção e complexidade do código. No entanto, popularidade não está diretamente relacionada à qualidade interna, sendo mais um reflexo de outros fatores como visibilidade e funcionalidade.
