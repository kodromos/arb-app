# services/bybit.py
import requests

BASE_URL = "https://api.bybit.com/v2/public/orderBook/L2"

async def get_prices(tokens):
    prices = {}
    for token in tokens:
        symbol = f"{token}USDT"
        try:
            response = requests.get(BASE_URL, params={"symbol": symbol})
            if response.status_code == 200:
                # Bybit precisa de ajustes no parsing, dados simplificados aqui
                prices[token] = {
                    "bid": 1.01,  # Simulado
                    "ask": 1.02,  # Simulado
                    "volume": 500  # Simulado
                }
        except Exception as e:
            print(f"Erro ao obter dados da Bybit para {token}: {e}")
    return prices