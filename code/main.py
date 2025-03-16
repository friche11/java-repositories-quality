from github_api import fetch_github_data
from data_formatter import process_repositories

if __name__ == "__main__":
    print(f" Buscando dados do GitHub...\n")
    try:
        
        raw_data = fetch_github_data()
        process_repositories(raw_data)

    except Exception as e:
        print(f" Houve um erro ao conectar com a API do Github: {e}")
