import requests

BASE_URL = "https://api.kucoin.com/api/v1/market/orderbook/level2_20"

async def get_prices(tokens):
    prices = {}
    for token in tokens:
        symbol = f"{token}-USDT"  # Par de negociação
        try:
            response = requests.get(BASE_URL, params={"symbol": symbol})
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    # Obtém o primeiro lance (bid) e oferta (ask)
                    bids = data["data"]["bids"]
                    asks = data["data"]["asks"]

                    prices[token] = {
                        "bid": float(bids[0][0]) if bids else None,  # Preço bid (ou None)
                        "ask": float(asks[0][0]) if asks else None,  # Preço ask (ou None)
                        "volume": float(min(bids[0][1], asks[0][1])) if bids and asks else 0  # Menor volume
                    }
            else:
                print(f"Erro na API KuCoin para {symbol}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição para KuCoin em {symbol}: {e}")
        except Exception as e:
            print(f"Erro desconhecido em {symbol}: {e}")
    return prices
