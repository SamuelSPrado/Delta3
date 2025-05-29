import requests
from DataBase import secret


def get_simple_sales(store_id, start, end):
    url = "https://meep-management.azure-api.net/third/sales/v1/GetSimpleSales"

    params = {
        'StoreId': store_id,
        'Start': start,
        'End': end
    }

    headers = {
        'Ocp-Apim-Subscription-Key': secret.OCP_KEY,
        'Authorization': f'{secret.TOKEN}'
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Erro na chamada à API: {e}")
