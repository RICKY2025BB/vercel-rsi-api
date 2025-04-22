import requests, pandas as pd
from ta.momentum import RSIIndicator

BOT_TOKEN = "7683062693:AAEiMtMEelshgXTCvbGau5be2JutIYECSxg"
CHAT_ID = "881405754"
BIRDEYE_API_KEY = "44b903b1ed4a49f7abef8264572daebf"

def handler(request):
    TOKEN_MAP = {
        "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgiXCa6xjnB7YaB1pPB263"
    }

    results = []

    for name, token_address in TOKEN_MAP.items():
        url = f"https://public-api.birdeye.so/public/price?address={token_address}"
        headers = {"X-API-KEY": BIRDEYE_API_KEY}
        try:
            res = requests.get(url, headers=headers).json()
            price = float(res["data"]["value"])
        except:
            continue

        history_url = f"https://public-api.birdeye.so/public/token_price/history?address={token_address}&interval=1m&span=15m"
        try:
            history_res = requests.get(history_url, headers=headers).json()
            historical_prices = [float(x[1]) for x in history_res["data"][-14:]]
        except:
            historical_prices = [price] * 14

        if len(historical_prices) < 14:
            continue

        rsi = RSIIndicator(pd.Series(historical_prices)).rsi().iloc[-1]

        if rsi < 30:
            msg = f"📉 RSI 预警\nToken: {name}\nRSI: {round(rsi,2)}\nPrice: ${price}"
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": msg}
            requests.post(telegram_url, data=payload)

        results.append(f"{name} RSI: {round(rsi,2)}")

    return {
        "statusCode": 200,
        "body": "\n".join(results)
    }
