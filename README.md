# Discord リアクションBot

特定のキーワードや絵文字文字列が含まれるメッセージに自動でリアクションを付けるDiscord Botです。GitHub Actionsによる自動時間管理で、Railway の月500時間制限内で効率的に運用されます。
治安が悪いDiscordサーバーで使われてるので、治安が悪いです（小泉構文
大体はAIに作ってもらって細かいところをカスタマイズしました。

## 🎯 主な機能

### 自動リアクション
- **キーワードマッチ**: メッセージに特定の単語が含まれていると自動でリアクション
- **カスタム絵文字対応**: サーバー独自の絵文字も使用可能
- **複数リアクション**: 1つのキーワードに対して複数のリアクションを設定可能
- **ランダム選択**: 複数候補からランダムに選んでリアクション
- **大文字小文字区別なし**: 柔軟なマッチング

### スラッシュコマンド
- `/reactions`: リアクションルール一覧を表示
- `/mynick`: 1日固定のあだ名をサーバーロールから決定（決定論的）

### 自動時間管理
- **GitHub Actions**: 毎日 AM10:00-AM2:00（JST）のみ稼働
- **月間稼働時間**: 480時間（Railway 500時間制限内で安全運用）
- **自動起動/停止**: 手動操作不要
- **Discord通知**: 起動・停止時にWebhookで通知

## 🛠️ セットアップ

### 前提条件
- Python 3.12
- Discord Bot アカウント
- Railway アカウント
- GitHub アカウント

### 必要な環境変数とシークレット

#### Railway 環境変数
```
DISCORD_TOKEN=your_discord_bot_token
```

#### GitHub リポジトリシークレット
```
RAILWAY_TOKEN=your_railway_api_token
RAILWAY_PROJECT_ID=your_railway_project_id
DISCORD_WEBHOOK_URL=your_discord_webhook_url_for_notifications
```

#### GitHub リポジトリ変数（自動設定）
```
RAILWAY_SERVICE_ID=auto_detected_service_id
```

### Railway デプロイ手順

1. **GitHubリポジトリ作成・プッシュ**
   ```bash
   git clone your-repo
   cd discord-bot
   git push origin main
   ```

2. **Railway プロジェクト作成**
   - Railway で新しいプロジェクト作成
   - GitHub リポジトリと連携

3. **環境変数設定**
   - Railway Dashboard で `DISCORD_TOKEN` を設定

4. **GitHub Actions 設定**
   - Repository Settings → Secrets で必要なシークレットを設定
   - Actions が有効になっていることを確認

5. **初回デプロイ**
   - 自動でデプロイが開始されます

## ⏰ 稼働スケジュール

GitHub Actions による自動時間管理：

| 項目 | 設定 | 説明 |
|------|------|------|
| **稼働時間** | 毎日 AM 10:00 - AM 2:00 (JST) | 16時間/日 |
| **停止時間** | 毎日 AM 2:00 - AM 10:00 (JST) | 8時間休止 |
| **月間稼働** | 約480時間 | 500時間制限内で安全 |
| **自動制御** | GitHub Actions Cron | 確実な時間管理 |
| **手動操作** | 可能 | start/stop/restart/status |

### 手動操作方法
GitHub Actions タブから「Discord Bot Scheduler」を手動実行：
- `start`: Bot起動
- `stop`: Bot停止  
- `restart`: Bot再起動
- `status`: 現在の状態確認

## 🔧 Discord Bot設定

### Discord Developer Portal 設定

**Bot Permissions（権限）:**
- ✅ View Channels (チャンネルを見る)
- ✅ Send Messages (メッセージを送信)
- ✅ Read Message History (メッセージ履歴を読む)
- ✅ **Add Reactions (リアクションを追加)** ← 重要！
- ✅ Use Slash Commands (スラッシュコマンドを使用)

**Privileged Gateway Intents（特権インテント）:**
- ✅ **Message Content Intent** ← 重要！

## 📁 ファイル構成

```
discord-bot/
├── main.py                           # メインBotコード
├── requirements.txt                  # Python依存関係
├── runtime.txt                      # Python バージョン指定
├── Procfile                         # Railway 起動設定
├── railway.toml                     # Railway 設定
├── .gitignore                       # Git 除外設定
├── .github/
│   └── workflows/
│       └── bot-scheduler.yml        # GitHub Actions自動管理
└── README.md                        # このファイル
```

## 🎭 リアクションルール

### リアクションルールのカスタマイズ
`main.py` の `REACTION_RULES` 辞書を編集：

```python
REACTION_RULES = {
  'キーワード': '絵文字',                    # 単一リアクション
  'キーワード2': ['絵文字1', '絵文字2'],      # 複数リアクション
  'キーワード3': {'random': ['絵文字A', 'B']}, # ランダム選択
}
```

## 💰 運用コスト比較

| サービス | プラン | 月額 | 稼働時間 | 自動管理 |
|---------|-------|------|----------|---------|
| **Railway** | **Hobby** | **$5** | **500時間** | ✅ |
| Render | Free | $0 | 750時間 | ❌（スリープあり） |
| Heroku | Basic | $7 | 無制限 | ❌ |

**Railway を選ぶ理由:**
- コスパが良い（$5/月）
- 確実な稼働時間管理
- GitHub Actions との相性が良い
- シンプルなデプロイプロセス

## 🔧 トラブルシューティング

### よくある問題

**1. Bot が反応しない**
- Discord Token が正しく設定されているか確認
- Message Content Intent が有効になっているか確認
- Bot に必要な権限があるか確認

**2. GitHub Actions が動かない**
- Repository Secrets が正しく設定されているか確認
- Railway API Token が有効か確認
- Actions が有効になっているか確認

**3. カスタム絵文字が動かない**
- 絵文字名が正しいか確認（大文字小文字注意）
- Bot がそのサーバーにいるか確認
- 絵文字のIDが正しいか確認

### ログ確認方法
- **Railway**: Dashboard のログセクション
- **GitHub Actions**: Actions タブの実行履歴
- **Discord**: Bot のコンソール出力
