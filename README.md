# Solana RSI Alert - Vercel API 版本

## 项目功能：
- 通过 Birdeye 获取 SOL 代币价格，计算 RSI
- 当 RSI < 30 时通过 Telegram 推送提醒

## 部署方式：
1. 上传到 GitHub 并导入 Vercel（不使用 cron）
2. 部署完成后，你将拥有公开接口，例如：
   https://your-vercel-domain.vercel.app/api/cron

## 实现定时运行：
使用 UptimeRobot 设置每分钟访问上面接口，即可自动运行！

无需绑定信用卡，永久免费方案兼容。
