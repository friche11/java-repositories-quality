import http.client
import json
import os
import csv
from dotenv import load_dotenv

# Carregar variáveis do .env explicitamente
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Testar se o GITHUB_TOKEN foi carregado corretamente
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("ERRO: GITHUB_TOKEN não foi carregado. Verifique seu arquivo .env!")
print(f"GITHUB_TOKEN carregado com sucesso: {TOKEN[:5]}...")

def load_query():
    """Carrega a query GraphQL a partir do arquivo `query.gql`."""
    query_path = os.path.join(os.path.dirname(__file__), "query.gql")
    
    if not os.path.exists(query_path):
        raise FileNotFoundError(f"Arquivo `query.gql` não encontrado em: {query_path}")
    
    with open(query_path, "r") as file:
        return file.read()

# Carrega a query e a URL da API
QUERY = load_query()
GITHUB_API_URL = "api.github.com"

def fetch_github_data(limit=100, batch_size=20):
    """Faz requisições paginadas à API do GitHub para obter até 1.000 repositórios de 20 em 20."""
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

def save_repositories_to_csv(repos, filename="repositories.csv"):
    """Salva os repositórios coletados em um arquivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nome", "Estrelas", "Criado em", "Forks", "Releases"])
        
        for repo in repos:
            writer.writerow([
                repo.get("name", "N/A"),
                repo.get("stargazerCount", 0),
                repo.get("createdAt", "N/A"),
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