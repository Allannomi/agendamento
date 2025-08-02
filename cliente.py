import requests

def criar_dados(local: str, data_hora: str, descricao: str) -> dict | None:
    """
    Envia os dados para a API criar um novo agendamento.

    Retorna um dicionário com a resposta da API em caso de sucesso,
    ou None se ocorrer um erro.
    """
    # URL do endpoint POST da sua API
    url = "http://127.0.0.1:8000/agendamentos/"
    
    # Monta o "pacote" de dados JSON que a API espera
    dados_para_enviar = {
        "local": local,
        "data_hora": data_hora,
        "descricao": descricao
    }

    try:
        # Faz o pedido POST, enviando os dados no corpo da requisição
        response = requests.post(url, json=dados_para_enviar, timeout=10)

        # Verifica se o agendamento foi CRIADO com sucesso (código 201)
        if response.status_code == 201:
            # Retorna os dados que a API enviou de volta (ex: o ID criado)
            return response.json()
        else:
            # Se a API retornou outro status, consideramos uma falha
            print(f"Erro da API: Status {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        # Captura erros de conexão, timeout, etc.
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