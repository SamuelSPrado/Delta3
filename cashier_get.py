import requests
from DataBase import secret

def get_cashier_info(caixa_id):
    url = f"https://meep-management.azure-api.net/third/cashier/v1/{caixa_id}"
    headers = {
        'Ocp-Apim-Subscription-Key': secret.OCP_KEY,
        'Authorization': f'{secret.TOKEN}'
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        data = resp.json()
        start = data.get('Start')
        end = data.get('End')

        if not all([start, end]):
            raise ValueError("Resposta da API não contém 'Start' ou 'End'.")

        return start, end

    except requests.HTTPError as e:
        raise RuntimeError(f"Erro HTTP: {e.response.status_code} - {e.response.text}")
    except requests.RequestException as e:
        raise RuntimeError(f"Erro de requisição: {e}")