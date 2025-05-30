# Discord リアクションBot

特定のキーワードや絵文字文字列が含まれるメッセージに自動でリアクションを付けるDiscord Botです。Railway Cronで自動的に時間管理され、月500時間以内で運用されます。

## 🎯 主な機能

### 自動リアクション
- **キーワードマッチ**: メッセージに特定の単語が含まれていると自動でリアクション
- **絵文字文字列マッチ**: `:poop:`、`:heart_eyes:` などの文字列に反応
- **カスタムパターン**: `:n_::ti_:`（見てる）、`www`（草）などの特殊パターン
- **大文字小文字区別なし**: 柔軟なマッチング
- **重複防止**: 同じメッセージに同じリアクションは1つまで

### 自動時間管理
- **Railway Cron**: 毎日 AM10:00-AM2:00（JST）のみ稼働
- **月間稼働時間**: 480時間（Railway無料枠500時間以内）
- **自動起動/停止**: 手動操作不要

## 🛠️ セットアップ

### 前提条件
- Python 3.12以上
- Discord Bot アカウント
- Railway アカウント

### Railway デプロイ

#### railway.toml使用

1. **GitHubリポジトリ作成・プッシュ**
2. **Railway と GitHub連携**
3. **環境変数設定**: `DISCORD_TOKEN`
4. **自動デプロイ完了！**

## ⏰ 稼働スケジュール

Railway Cronによる自動時間管理：

| 項目 | 設定 |
|------|------|
| **稼働時間** | 毎日 AM 10:00 - AM 2:00 (JST) |
| **停止時間** | 毎日 AM 2:00 - AM 10:00 (JST) |
| **1日稼働** | 16時間 |
| **月間稼働** | 480時間 (500時間制限内 ✅) |
| **自動制御** | Railway Cron |

## 🔧 Discord Bot設定

### 必要な権限
Discord Developer Portalで以下を設定：

**Bot Permissions:**
- ✅ View Channels (チャンネルを見る)
- ✅ Send Messages (メッセージを送信)
- ✅ Read Message History (メッセージ履歴を読む)
- ✅ **Add Reactions (リアクションを追加)** ← 重要！
- ✅ Use Slash Commands (スラッシュコマンドを使用)

**Privileged Gateway Intents:**
- ✅ **Message Content Intent** ← 重要！

### Bot招待URL生成
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=68672&scope=bot%20applications.commands
```

## 📁 ファイル構成

```
discord-bot/
├── main.py              # メインBot
├── railway.toml         # Railway Cron設定
├── requirements.txt     # Python依存関係
├── Procfile            # Railway起動設定
├── .gitignore          # Git除外設定
└── README.md           # このファイル
```

## 💰 コスト

| サービス | プラン | 月額 | 稼働時間 |
|---------|-------|------|----------|
| **Railway** | **Hobby** | **$5** | **500時間** |
| Render | Free | $0 | 750時間（スリープあり） |
| Heroku | Basic | $7 | 無制限 |

Railway Hobbyプランが最もコスパが良く、Cron機能で確実に制限内で運用できます。

### 稼働時間変更
`railway.toml`のCron設定を変更：
```toml
[cron]
start = "0 9 * * *"   # JST 18:00起動
stop = "0 15 * * *"   # JST 翌日00:00停止
```
