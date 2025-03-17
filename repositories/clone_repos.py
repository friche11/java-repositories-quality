import os
import csv
import subprocess
import time

# Nome do arquivo CSV que contém a lista de repositórios
CSV_FILE = "repositories.csv"
# Pasta onde os repositórios serão clonados
REPOS_DIR = "repositories"
# Tempo de espera entre cada clone para evitar bloqueios (em segundos)
DELAY_BETWEEN_CLONES = 5

def read_repositories():
    """Lê os repositórios do arquivo CSV e retorna uma lista de URLs do GitHub."""
    repositories = []
    
    if not os.path.exists(CSV_FILE):
        print(f"ERRO: O arquivo {CSV_FILE} não foi encontrado!")
        return []
    
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pular cabeçalho
        for row in reader:
            if len(row) < 2:
                continue
            owner = row[1].strip()  # OWNER do repositório
            repo_name = row[0].strip()  # Nome do repositório
            full_repo_name = f"{owner}/{repo_name}"
            repo_url = f"https://github.com/{full_repo_name}.git"
            repositories.append((full_repo_name, repo_url))
    
    return repositories

def clone_repository(repo_name, repo_url):
    """Clona um repositório do GitHub se ainda não foi baixado."""
    repo_path = os.path.join(REPOS_DIR, repo_name.replace("/", "_"))
    
    if os.path.exists(repo_path):
        print(f"Repositório {repo_name} já foi clonado. Pulando...")
        return
    
    print(f"Clonando {repo_name}...")
    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        print(f"Repositório {repo_name} clonado com sucesso!")
    except subprocess.CalledProcessError:
        print(f"Erro ao clonar {repo_name}")
    
    time.sleep(DELAY_BETWEEN_CLONES)

def main():
    """Executa o processo de clonagem dos repositórios."""
    os.makedirs(REPOS_DIR, exist_ok=True)
    repositories = read_repositories()
    
    if not repositories:
        print("Nenhum repositório encontrado no CSV. Certifique-se de que o arquivo está correto!")
        return
    
    for repo_name, repo_url in repositories:
        clone_repository(repo_name, repo_url)
    
    print("Todos os repositórios foram clonados!")

if __name__ == "__main__":
    main()
