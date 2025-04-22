import requests
import statistics

BOT_TOKEN = "7683062693:AAEiMtMEelshgXTCvbGau5be2JutIYECSxg"
CHAT_ID = "881405754"
BIRDEYE_API_KEY = "44b903b1ed4a49f7abef8264572daebf"

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]
    avg_gain = statistics.mean(gains[-period:])
    avg_loss = statistics.mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def handler(request):
    try:
        TOKEN_MAP = {
            "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgiXCa6xjnB7YaB1pPB263"
        }

        results = []
        for name, token_address in TOKEN_MAP.items():
            headers = {"X-API-KEY": BIRDEYE_API_KEY}

            price_url = f"https://public-api.birdeye.so/public/price?address={token_address}"
            price_res = requests.get(price_url, headers=headers).json()
            price = float(price_res["data"]["value"])

            hist_url = f"https://public-api.birdeye.so/public/token_price/history?address={token_address}&interval=1m&span=30m"
            hist_res = requests.get(hist_url, headers=headers).json()
            prices = [float(p[1]) for p in hist_res["data"][-15:]]

            rsi = calculate_rsi(prices)
            results.append(f"{name} RSI: {round(rsi, 2)}")

            if rsi is not None and rsi < 30:
                message = f"📉 RSI 预警\n{name}\nRSI: {round(rsi, 2)}\nPrice: ${price}"
                tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(tg_url, data={"chat_id": CHAT_ID, "text": message})

        return {"statusCode": 200, "body": "\n".join(results)}

    except Exception as e:
        return {"statusCode": 500, "body": f"❌ Error: {str(e)}"}
