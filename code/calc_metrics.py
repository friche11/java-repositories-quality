import pandas as pd
import os
import subprocess
import numpy as np
import subprocess
import os

def executar_ck():
    """Executa CK em todos os repositórios clonados e continua mesmo se um falhar."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    REPOS_DIR = os.path.join(BASE_DIR, "repositories")
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "ck")
    CK_JAR_PATH = os.path.join(BASE_DIR, "ck", "target", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
    ERROR_LOG_PATH = os.path.join(BASE_DIR, "logs", "ck_errors.log")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)

    repositorios = [repo for repo in os.listdir(REPOS_DIR) if os.path.isdir(os.path.join(REPOS_DIR, repo))]

    for repo in repositorios:
        repo_path = os.path.join(REPOS_DIR, repo)
        repo_output_folder = os.path.join(OUTPUT_DIR, repo)
        os.makedirs(repo_output_folder, exist_ok=True)

        ck_command = [
            "java", "-jar", CK_JAR_PATH,
            repo_path, "false", "0", "false"
        ]

        print(f"Executando CK no repositório: {repo}...")

        try:
            subprocess.run(ck_command, check=True, cwd=repo_output_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"CK finalizado para {repo}")
        except subprocess.CalledProcessError as e:
            error_message = f"Erro ao executar CK em {repo}: {e}\n"
            print(error_message)

            # Registrar erro no arquivo de log
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(error_message)
        
        except Exception as e:
            error_message = f"Erro inesperado em {repo}: {e}\n"
            print(error_message)

            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(error_message)

    print(f"\nProcessamento concluído! Logs de erro (se houver) foram salvos em {ERROR_LOG_PATH}")

def analisar_dados():
    """Analisa os dados separando repositórios pela mediana das variáveis de análise."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    RESULTADOS_PATH = os.path.join(BASE_DIR, "docs", "resultados.csv")

    if not os.path.exists(RESULTADOS_PATH):
        print(f"Arquivo não encontrado: {RESULTADOS_PATH}")
        return

    # Carregar os dados
    df = pd.read_csv(RESULTADOS_PATH)

    # Variáveis de análise
    variaveis_analise = ["Estrelas", "Maturidade (anos)", "Releases", "Linhas de Código (LOC)"]
    metricas_qualidade = ["Acoplamento Entre Objetos (CBO)", 
                          "Profundidade da Árvore de Herança (DIT)", 
                          "Falta de Coesão dos Métodos (LCOM)", 
                          "Linhas de Código (LOC)"]

    # Criar classificações por mediana
    for var in variaveis_analise:
        mediana = df[var].median()
        df[f"{var}_Grupo"] = df[var].apply(lambda x: "Alto" if x >= mediana else "Baixo")

    # Criar lista para armazenar os resultados
    resultados = []

    # Gerar estatísticas por grupo e salvar corretamente
    for var in variaveis_analise:
        grupo_coluna = f"{var}_Grupo"

        if grupo_coluna not in df.columns:
            print(f"Coluna {grupo_coluna} não encontrada no DataFrame.")
            continue

        estatisticas = df.groupby(grupo_coluna)[metricas_qualidade].agg(["mean", "median", "std"]).round(2)

        # Adicionar os dados formatados à lista de resultados
        for grupo in estatisticas.index:
            for metrica in metricas_qualidade:
                resultados.append([var, grupo, metrica, "Média", estatisticas.loc[grupo, (metrica, "mean")]])
                resultados.append([var, grupo, metrica, "Mediana", estatisticas.loc[grupo, (metrica, "median")]])
                resultados.append([var, grupo, metrica, "Desvio Padrão", estatisticas.loc[grupo, (metrica, "std")]])

    # Converter lista de resultados para DataFrame
    df_resultados = pd.DataFrame(resultados, columns=["Variável de Análise", "Grupo", "Métrica", "Tipo", "Valor"])

    # Salvar o arquivo CSV corretamente formatado
    ANALISE_PATH = os.path.join(BASE_DIR, "docs", "analise_resultados.csv")
    df_resultados.to_csv(ANALISE_PATH, index=False, encoding="utf-8")

    print(f"\nAnálise concluída! Resultados salvos em {ANALISE_PATH}")


def gerar_planilha_resultados():
    """Gera a planilha consolidada de resultados combinando CK com repositories.csv."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CK_DIR = os.path.join(BASE_DIR, "outputs", "ck")
    DOCS_DIR = os.path.join(BASE_DIR, "docs")
    os.makedirs(DOCS_DIR, exist_ok=True)

    quality_metrics = {
        "cbo": "Acoplamento Entre Objetos (CBO)",
        "dit": "Profundidade da Árvore de Herança (DIT)",
        "lcom": "Falta de Coesão dos Métodos (LCOM)",
        "loc": "Linhas de Código (LOC)"
    }

    data_list = []
    if not os.path.exists(CK_DIR):
        print(f"Diretório não encontrado: {CK_DIR}")
        return

    for repo_name in os.listdir(CK_DIR):
        repo_path = os.path.join(CK_DIR, repo_name)
        if not os.path.isdir(repo_path):
            continue

        # Caminhos dos arquivos de métricas
        class_metrics_path = os.path.join(repo_path, "class.csv")
        method_metrics_path = os.path.join(repo_path, "method.csv")
        summary_output_path = os.path.join(repo_path, "summary_metrics.csv")

        # Lista para armazenar os DataFrames
        metrics_dataframes = []

        # Carregar métricas de classes, se existir e não estiver vazio
        if os.path.exists(class_metrics_path) and os.path.getsize(class_metrics_path) > 0:
            try:
                class_metrics = pd.read_csv(class_metrics_path)
                metrics_dataframes.append(class_metrics)
            except pd.errors.EmptyDataError:
                print(f"Aviso: {class_metrics_path} está vazio. Será substituído por valores em branco.")

        # Carregar métricas de métodos, se existir e não estiver vazio
        if os.path.exists(method_metrics_path) and os.path.getsize(method_metrics_path) > 0:
            try:
                method_metrics = pd.read_csv(method_metrics_path)
                metrics_dataframes.append(method_metrics)
            except pd.errors.EmptyDataError:
                print(f"Aviso: {method_metrics_path} está vazio. Será substituído por valores em branco.")

        # Se nenhum dado foi carregado, adiciona linha vazia para manter estrutura
        if not metrics_dataframes:
            print(f"Nenhum dado encontrado para {repo_name}. Inserindo linha vazia.")
            empty_row = {col: np.nan for col in quality_metrics.keys()}
            empty_row["Repositório"] = repo_name.strip().lower()
            data_list.append(pd.DataFrame([empty_row]))
            continue

        # Concatenar os DataFrames
        combined_metrics = pd.concat(metrics_dataframes, ignore_index=True)

        # Selecionar apenas as métricas disponíveis
        available_metrics = [col for col in quality_metrics if col in combined_metrics.columns]

        if not available_metrics:
            print(f"Nenhuma métrica válida encontrada em {repo_name}")
            continue

        # Gerar estatísticas de resumo
        summary = combined_metrics[available_metrics].agg(["mean", "median", "std"]).reset_index()
        summary[available_metrics] = summary[available_metrics].round(2)
        summary.rename(columns={col: quality_metrics[col] for col in available_metrics}, inplace=True)
        summary.replace({"mean": "Média", "median": "Mediana", "std": "Desvio Padrão"}, inplace=True)
        summary.rename(columns={"index": "Medida"}, inplace=True)

        repo_clean_name = repo_name.split("_", 1)[-1] if "_" in repo_name else repo_name
        summary.insert(0, "Repositório", repo_clean_name.strip().lower())

        # Salvar o sumário individual
        summary.to_csv(summary_output_path, index=False, encoding="utf-8")
        data_list.append(summary)

    if not data_list:
        print("Nenhum sumário encontrado. Processo encerrado.")
        return

    # Unir todos os sumários individuais em um único DataFrame
    summary_df = pd.concat(data_list, ignore_index=True)

    repositories_path = os.path.join(BASE_DIR, "outputs", "repositories.csv")
    if not os.path.exists(repositories_path):
        print(f"Arquivo não encontrado: {repositories_path}")
        return

    # Carregar os dados dos repositórios e mesclar com os sumários de métricas
    repositories_df = pd.read_csv(repositories_path)
    resultados_df = pd.merge(repositories_df, summary_df, on="Repositório", how="left")
    
    resultados_path = os.path.join(DOCS_DIR, "resultados.csv")
    resultados_df.to_csv(resultados_path, index=False, encoding="utf-8")

    print(f"Resultados salvos em: {resultados_path}")

def main():
    """Menu principal para o usuário escolher a ação."""
    while True:
        print("\nMenu Principal")
        print("1 - Executar CK nos repositórios clonados")
        print("2 - Gerar planilha de resultados")
        print("3 - Analisar dados separando repositórios pela mediana")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            executar_ck()
        elif opcao == "2":
            gerar_planilha_resultados()
        elif opcao == "3":
            analisar_dados()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
