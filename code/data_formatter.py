from datetime import datetime
from tabulate import tabulate

def process_repositories(repos):
    """ Processa e formata os dados para exibição no console. """
    formatted_data = []

    for repo in repos:
        created_at = datetime.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")

        # Cálculo da maturidade em anos
        age_years = round((datetime.utcnow() - created_at).days / 365, 2)

        formatted_data.append([
            repo["name"],
            repo["stargazerCount"],
            age_years,
            repo["releases"]["totalCount"]
        ])

    headers = ["Nome", "Estrelas", "Maturidade (anos)", "Releases"]
    print(tabulate(formatted_data, headers=headers, tablefmt="fancy_grid"))
