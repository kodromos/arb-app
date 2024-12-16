import requests

BASE_URL = "https://api.mercadobitcoin.net/api/v4/ticker/"

async def get_prices(tokens):
    prices = {}
    for token in tokens:
        symbol = f"{token}USDT"
        try:
            response = requests.get(BASE_URL, params={"symbol": symbol})
            if response.status_code == 200:
                data = response.json()
                prices[token] = {
                    "bid": float(data["bidPrice"]),
                    "ask": float(data["askPrice"]),
                    "volume": 1000  # Valor simulado, ajustar para dados reais
                }
        except Exception as e:
            print(f"Erro ao obter dados da Binance para {token}: {e}")
    return prices