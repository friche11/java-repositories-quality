import http.client
import json
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis do .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Testar se o GITHUB_TOKEN foi carregado corretamente
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("ERRO: GITHUB_TOKEN não foi carregado. Verifique seu arquivo .env!")

GITHUB_API_URL = "api.github.com"

def load_query():
    """Carrega a query GraphQL a partir do arquivo `query.gql`."""
    query_path = os.path.join(os.path.dirname(__file__), "query.gql")
    
    if not os.path.exists(query_path):
        raise FileNotFoundError(f"Arquivo `query.gql` não encontrado em: {query_path}")
    
    with open(query_path, "r") as file:
        return file.read()

QUERY = load_query()

def fetch_github_data(limit=1000, batch_size=20):
    """Faz requisições paginadas à API do GitHub para obter repositórios."""
    conn = http.client.HTTPSConnection(GITHUB_API_URL)
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Python-Request"
    }
    
    repos = []
    after_cursor = None  
    
    while len(repos) < limit:
        variables = {"after": after_cursor, "first": batch_size}
        request_body = json.dumps({"query": QUERY, "variables": variables})
        
        conn.request("POST", "/graphql", body=request_body, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        if "errors" in data:
            print("Erro ao requisitar API do GitHub:", data["errors"])
            break
        
        search_results = data.get("data", {}).get("search", {})
        new_repos = [edge["node"] for edge in search_results.get("edges", [])]
        
        if not new_repos:
            print("Nenhum novo repositório encontrado. Encerrando...")
            break
        
        repos.extend(new_repos)
        has_next_page = search_results.get("pageInfo", {}).get("hasNextPage", False)
        after_cursor = search_results.get("pageInfo", {}).get("endCursor")
        
        print(f"Obtidos {len(new_repos)} novos repositórios. Total até agora: {len(repos)}")
        
        if not has_next_page or len(repos) >= limit:
            break
    
    conn.close()
    save_repositories_to_csv(repos)
    return repos[:limit]

def save_repositories_to_csv(repos):
    """Salva os repositórios coletados em um arquivo CSV dentro da pasta ../outputs/"""
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)  # Garante que a pasta exista

    filename = os.path.join(output_dir, "repositories.csv")

    # Criação/Substituição do arquivo CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Repositório", "Dono", "Estrelas", "Maturidade (anos)", "Forks", "Releases"])
        
        for repo in repos:
            created_at = datetime.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
            age_years = round((datetime.utcnow() - created_at).days / 365, 2)

            writer.writerow([
                repo.get("name", "N/A"),
                repo.get("owner", {}).get("login", "N/A"),
                repo.get("stargazerCount", 0),
                age_years,
                repo.get("forkCount", 0),
                repo.get("releases", {}).get("totalCount", 0)
            ])
    
    print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    print("Buscando dados do GitHub...\n")
    try:
        fetch_github_data()
    except Exception as e:
        print(f"Houve um erro ao conectar com a API do GitHub: {e}")
