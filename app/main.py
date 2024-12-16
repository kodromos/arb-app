# crypto_arbitrage/main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
from services import binance, bybit, kucoin, mercado_bitcoin

# Lista de altcoins de interesse
TOKENS = ["ADA", "NEAR", "AAVE", "LINK", "DOT", "TIA", "JASMY", "DOGE", "ALGO", "RUNE", "FET", "SAND", "GMX"]

# Configurações de arbitragem
SPREAD_MINIMO = 2.0  # Spread mínimo para exibir
VOLUME_MINIMO_USD = 500  # Valor mínimo em tokens para considerar a oportunidade
TAXA_FIXA_USD = 10  # Taxa fixa estimada para cada transação

# Inicializa o FastAPI
app = FastAPI()

# Função para calcular spreads
async def calcular_arbitragem():
    oportunidades = []

    # Consulta de preços em diferentes corretoras
    tasks = [
        binance.get_prices(TOKENS),
        bybit.get_prices(TOKENS),
        kucoin.get_prices(TOKENS),
        mercado_bitcoin.get_prices(TOKENS)
    ]
    results = await asyncio.gather(*tasks)

    precos = {
        "binance": results[0],
        "bybit": results[1],
        "kucoin": results[2],
        "mercado_bitcoin": results[3]
    }

    # Comparar preços entre corretoras
    for token in TOKENS:
        for compra_corretora, precos_compra in precos.items():
            for venda_corretora, precos_venda in precos.items():
                if compra_corretora != venda_corretora and token in precos_compra and token in precos_venda:
                    preco_compra = precos_compra[token]["ask"]
                    preco_venda = precos_venda[token]["bid"]
                    volume_disponivel = min(precos_compra[token]["volume"], precos_venda[token]["volume"])

                    if preco_compra and preco_venda and volume_disponivel:
                        # Calcula o spread
                        spread_percentual = ((preco_venda - preco_compra) / preco_compra) * 100

                        # Filtra pelo volume e spread mínimo
                        if spread_percentual >= SPREAD_MINIMO and (volume_disponivel * preco_compra) >= VOLUME_MINIMO_USD:
                            oportunidades.append({
                                "token": token,
                                "compra_em": compra_corretora,
                                "venda_em": venda_corretora,
                                "spread": round(spread_percentual, 2),
                                "volume": round(volume_disponivel, 2),
                                "taxas_estimadas": TAXA_FIXA_USD * 2  # compra e venda
                            })

    return oportunidades

# Rota principal
@app.get("/oportunidades")
async def oportunidades():
    try:
        arbitragem = await calcular_arbitragem()
        return JSONResponse(content={"oportunidades": arbitragem})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
