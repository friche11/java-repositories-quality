import http.client
import json
import os
from dotenv import load_dotenv 

# Carregar variáveis do .env
load_dotenv()

def load_query():
    """Carrega a query GraphQL a partir do arquivo `query.gql`."""
    query_path = os.path.join(os.path.dirname(__file__), "query.gql")
    
    if not os.path.exists(query_path):
        raise FileNotFoundError(f" Arquivo `query.gql` não encontrado em: {query_path}")
    
    with open(query_path, "r") as file:
        return file.read()

# Carrega a query e o token do GitHub
QUERY = load_query()
TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API_URL = "api.github.com"

def fetch_github_data(limit=60):
    """Faz requisições paginadas à API do GitHub para obter repositórios."""

    if not TOKEN:
        raise ValueError(" GITHUB_TOKEN não está definido. Configure a variável de ambiente.")

    conn = http.client.HTTPSConnection(GITHUB_API_URL)

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Python-Request"
    }

    repos = []
    after_cursor = None  

    while len(repos) < limit:
        variables = {"after": after_cursor}
        request_body = json.dumps({"query": QUERY, "variables": variables})
        
        conn.request("POST", "/graphql", body=request_body, headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        if "errors" in data:
            print(" Erro ao requisitar API do GitHub:", data["errors"])
            print("\n🔹 Tente diminuir a quantidade de repositórios a serem consultados em uma única requisição.")
            break

        search_results = data.get("data", {}).get("search", {})

        # Extração dos repositórios encontrados na busca
        new_repos = [edge["node"] for edge in search_results.get("edges", [])]
        if not new_repos:
            print(" Nenhum novo repositório encontrado, encerrando paginação.")
            break

        repos.extend(new_repos)

        # Atualiza paginação
        has_next_page = search_results.get("pageInfo", {}).get("hasNextPage", False)
        after_cursor = search_results.get("pageInfo", {}).get("endCursor")

        print(f" Obtidos {len(new_repos)} novos repositórios. Total até agora: {len(repos)}\n")

        if not has_next_page or len(repos) >= limit:
            break

    conn.close()
    return repos[:limit]
