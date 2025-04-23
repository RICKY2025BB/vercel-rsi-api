def handler(request):
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": '{"message": "✅ Solana RSI 接口运行正常！"}'
    }
