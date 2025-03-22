import pandas as pd
import os

# Diretório base onde os CSVs estão armazenados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CK_DIR = os.path.join(BASE_DIR, "outputs", "ck")

# Definir métricas de qualidade a serem analisadas
quality_metrics = {
    "cbo": "Acoplamento Entre Objetos (CBO)",
    "dit": "Profundidade da Árvore de Herança (DIT)",
    "lcom": "Falta de Coesão dos Métodos (LCOM)",
    "loc": "Linhas de Código (LOC)"
}

# Lista para armazenar os dados dos sumários
data_list = []

# Percorrer todos os repositórios dentro de outputs/ck/
if not os.path.exists(CK_DIR) or not os.path.isdir(CK_DIR):
    print(f"Diretório não encontrado: {CK_DIR}")
    exit()

for repo_name in os.listdir(CK_DIR):
    repo_path = os.path.join(CK_DIR, repo_name)

    # Verificar se é um diretório (para garantir que é um repositório)
    if not os.path.isdir(repo_path):
        continue

    # Caminho do CSV de métricas
    class_metrics_path = os.path.join(repo_path, "metricsclass.csv")
    output_path = os.path.join(repo_path, "summary_metrics.csv")

    if not os.path.exists(class_metrics_path):
        print(f"Arquivo não encontrado: {class_metrics_path}")
        continue

    # Carregar CSV de métricas de classe
    class_metrics = pd.read_csv(class_metrics_path)

    # Filtrar apenas as métricas disponíveis
    available_metrics = [col for col in quality_metrics if col in class_metrics.columns]
    
    if not available_metrics:
        print(f"Nenhuma métrica de qualidade encontrada para {repo_name}!")
        continue

    # Calcular estatísticas por repositório
    grouped = class_metrics[available_metrics]
    summary = grouped.agg(["mean", "median", "std"]).reset_index()

    # Arredondar os valores numéricos para duas casas decimais
    summary[available_metrics] = summary[available_metrics].round(2)

    # Traduzir colunas para português
    summary.rename(columns={col: quality_metrics[col] for col in available_metrics}, inplace=True)

    # Traduzir estatísticas
    summary.replace({
        "mean": "Média",
        "median": "Mediana",
        "std": "Desvio Padrão"
    }, inplace=True)

    # Renomear a coluna do índice para "Medida"
    summary.rename(columns={"index": "Medida"}, inplace=True)

    # Extrair apenas o nome do repositório (removendo o dono)
    repo_clean_name = repo_name.split("_", 1)[-1] if "_" in repo_name else repo_name

    # Adicionar nome do repositório
    summary.insert(0, "Repositório", repo_clean_name.strip().lower())

    # Salvar dentro da pasta do próprio repositório
    summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Sumarização salva em: {output_path}")

    # Adicionar ao consolidado
    data_list.append(summary)

# Criar dataframe consolidado de summary_metrics (apenas em memória)
if not data_list:
    print("Nenhum sumário encontrado. Processo encerrado.")
    exit()

summary_df = pd.concat(data_list, ignore_index=True)

# Carregar repositories.csv
repositories_path = os.path.join(BASE_DIR, "outputs", "repositories.csv")

if not os.path.exists(repositories_path):
    print(f"Arquivo não encontrado: {repositories_path}")
    exit()

repositories_df = pd.read_csv(repositories_path)

# Juntar os dados
resultados_df = pd.merge(repositories_df, summary_df, left_on="Repositório", right_on="Repositório", how="left")

# Salvar a planilha final com os resultados
resultados_path = os.path.join(BASE_DIR, "docs", "resultados.csv")
resultados_df.to_csv(resultados_path, index=False, encoding="utf-8")
print(f"Resultados salvos em: {resultados_path}")

print("Processo finalizado.")
