import os
import csv
import subprocess
import time

# Caminho base do projeto (subindo um nível a partir de "code/")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")  # Pasta 'outputs'
CSV_FILE = os.path.join(OUTPUTS_DIR, "repositories.csv")  # Caminho do CSV dentro de 'outputs'
REPOS_DIR = os.path.join(BASE_DIR, "repositories")  # Agora os repositórios serão clonados fora de 'code/'

DELAY_BETWEEN_CLONES = 5  # Tempo de espera entre clones (segundos)
MAX_ATTEMPTS = 1  # Número máximo de tentativas por repositório

def read_repositories():
    """Lê os repositórios do arquivo CSV dentro de 'outputs/' e retorna uma lista de URLs do GitHub."""
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
    """Clona um repositório do GitHub com tentativas e delay dinâmico."""
    repo_path = os.path.join(REPOS_DIR, repo_name.replace("/", "_"))  # Evita problema com '/'
    
    if os.path.exists(repo_path):
        print(f"Repositório {repo_name} já foi clonado. Pulando...")
        return True  # Considera como sucesso

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Tentativa {attempt}/{MAX_ATTEMPTS}: Clonando {repo_name}...")
        try:
            subprocess.run(["git", "clone", "--depth=1", repo_url, repo_path], check=True)
            print(f"✅ Repositório {repo_name} clonado com sucesso!")
            return True  # Clone bem-sucedido
        except subprocess.CalledProcessError:
            print(f"⚠ Erro ao clonar {repo_name}. Aguardando {DELAY_BETWEEN_CLONES} segundos antes de tentar novamente...")
            time.sleep(DELAY_BETWEEN_CLONES)  # Aguarda antes de tentar novamente

    print(f"❌ Falha ao clonar {repo_name} após {MAX_ATTEMPTS} tentativas.")
    return False  # Clone falhou

def main(max_clones):
    """Executa o processo de clonagem dos repositórios até atingir 'max_clones' com sucesso."""
    os.makedirs(REPOS_DIR, exist_ok=True)  # Garante que a pasta existe
    repositories = read_repositories()
    
    if not repositories:
        print("Nenhum repositório encontrado no CSV. Certifique-se de que o arquivo está correto!")
        return

    cloned_count = 0
    failed_repos = []
    
    for repo_name, repo_url in repositories:
        if cloned_count >= max_clones:
            break  # Para quando atingir o número desejado

        success = clone_repository(repo_name, repo_url)
        if success:
            cloned_count += 1
        else:
            failed_repos.append(repo_name)

    print("\n")
    print(f"✅ Repositórios clonados com sucesso: {cloned_count}/{max_clones}")
    if failed_repos:
        print(f"❌ Repositórios que falharam: {', '.join(failed_repos)}")
    else:
        print("Todos os repositórios desejados foram clonados com sucesso!")

if __name__ == "__main__":
    max_clones = int(input("Quantos repositórios deseja clonar? "))
    main(max_clones)
