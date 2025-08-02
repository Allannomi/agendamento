import requests

def criar_dados(local: str, data_hora: str, descricao: str) -> dict | None:
    url = "http://127.0.0.1:8000/agendamentos/"
    dados_para_enviar = {
        "local": local,
        "data_hora": data_hora,
        "descricao": descricao
    }
    try:
        response = requests.post(url, json=dados_para_enviar, timeout=10)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Erro da API: Status {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
        return None
    

def historicos():
    url = f"http://127.0.0.1:8000/historico"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None
    


def apagar(id_agendamento:int):
    url = f"http://127.0.0.1:8000/apagar/{id_agendamento}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return None
    except requests.exceptions.RequestException:
        return None