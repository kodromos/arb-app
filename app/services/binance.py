import requests

BASE_URL = "https://api.binance.com"

def fetch_binance_data(symbol: str):
    """Coleta preços do símbolo específico na Binance."""
    endpoint = f"{BASE_URL}/api/v3/ticker/bookTicker"
    params = {"symbol": symbol.upper()}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()  # Retorna os dados brutos
    else:
        return None
