# Discord リアクションBot (Gesuido Bot)

特定のキーワードや絵文字文字列が含まれるメッセージに自動でリアクションを付けるDiscord Botです。Docker環境で安定稼働し、24時間運用可能です。  
治安が悪いDiscordサーバーで使われてるので、治安が悪いです（小泉構文  
大体はAIに作ってもらって細かいところをカスタマイズしました。  

## 🎯 主な機能

### 自動リアクション
- **キーワードマッチ**: メッセージに特定の単語が含まれていると自動でリアクション
- **カスタム絵文字対応**: サーバー独自の絵文字も使用可能
- **複数リアクション**: 1つのキーワードに対して複数のリアクションを設定可能
- **ランダム選択**: 複数候補からランダムに選んでリアクション
- **大文字小文字区別なし**: 柔軟なマッチング
- **スペース無視**: 全角・半角スペースを無視してマッチング

### スラッシュコマンド
- `/reactions`: リアクションルール一覧を表示
- `/mynick`: 1日固定のあだ名をサーバーロールから決定（決定論的）
- `/spice`: 調味料スロット
- `/sex`: ちんぽスロット

### Docker運用
- **コンテナ化**: 環境分離による安定稼働
- **自動再起動**: 異常終了時の自動復旧
- **ログ管理**: 詳細なログ記録とローテーション
- **リソース制限**: メモリ・CPU使用量制限
- **ヘルスチェック**: 自動稼働監視

## 🛠️ セットアップ

### 前提条件
- Docker & Docker Compose
- Discord Bot アカウント

### インストール手順

#### 1. リポジトリクローン
```bash
git clone https://github.com/your-username/gesuido_bot.git
cd gesuido_bot
```

#### 2. Docker環境確認
```bash
# Dockerインストール確認
docker --version
docker compose version

# 未インストールの場合（Ubuntu）
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
# ログアウト・ログイン
```

#### 3. セットアップ実行
```bash
# セットアップスクリプト実行
chmod +x docker_setup.sh docker_bot.sh
./docker_setup.sh
```

#### 4. 環境変数設定
```bash
# .envファイル編集
nano .env
```

`.env`ファイルの設定例：
```bash
# Discord Bot Token (必須)
DISCORD_TOKEN=your_actual_discord_bot_token

# 特定ユーザー設定 (オプション)
TOMATO_USER=123456789012345678
```

#### 5. Bot起動
```bash
# Docker Composeで起動
docker compose up -d

# または管理スクリプト使用
./docker_bot.sh start
```

## 🔧 Bot管理

### 基本操作
```bash
./docker_bot.sh start      # Bot起動
./docker_bot.sh stop       # Bot停止
./docker_bot.sh restart    # Bot再起動
./docker_bot.sh status     # ステータス確認
./docker_bot.sh logs       # ログ表示
./docker_bot.sh logs -f    # リアルタイムログ監視
```

### 開発・メンテナンス
```bash
./docker_bot.sh shell      # コンテナ内にシェル接続
./docker_bot.sh update     # ソース変更後の更新
./docker_bot.sh clean      # Dockerリソースクリーンアップ
./docker_bot.sh backup     # 設定ファイルバックアップ
```

### 直接Docker操作
```bash
# 基本操作
docker compose up -d       # 起動
docker compose down        # 停止
docker compose restart     # 再起動
docker compose logs -f     # ログ監視

# メンテナンス
docker compose build       # イメージ再ビルド
docker stats gesuido_bot   # リソース監視
```

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
gesuido_bot/
├── main.py                    # メインBotコード
├── requirements.txt           # Python依存関係
├── .env                      # 環境変数設定
├── .gitignore               # Git除外設定
├── Dockerfile               # Dockerイメージ定義
├── docker-compose.yml       # Docker Compose設定
├── .dockerignore           # Docker除外設定
├── docker_setup.sh         # Docker初期セットアップ
├── docker_bot.sh           # Docker Bot管理スクリプト
├── .python-version         # pyenvバージョン指定
├── logs/                   # ログディレクトリ
└── README.md               # このファイル
```

## 🎭 リアクションルール

### カスタマイズ方法
1. `main.py`の`REACTION_RULES`辞書を編集
2. Bot再起動で反映：`./docker_bot.sh restart`

## 📊 監視・ログ

### ステータス確認
```bash
# 総合ステータス
./docker_bot.sh status

# リソース使用量
docker stats gesuido_bot

# ヘルスチェック
docker inspect gesuido_bot | grep Health -A 10
```

### ログ管理
```bash
# 最新ログ
./docker_bot.sh logs

# リアルタイム監視
./docker_bot.sh logs -f

# ログファイル直接確認
ls -la logs/
```

## 🔧 トラブルシューティング

### よくある問題

**1. Bot が反応しない**
```bash
# ステータス確認
./docker_bot.sh status

# ログ確認
./docker_bot.sh logs

# 再起動
./docker_bot.sh restart
```

**2. コンテナが起動しない**
```bash
# ログで原因確認
docker compose logs

# 設定ファイル確認
cat .env
cat docker-compose.yml
```

**3. メモリ不足**
```bash
# リソース使用量確認
docker stats gesuido_bot

# 制限調整（docker-compose.yml）
# deploy.resources.limits.memory を変更
```

**4. ログディスク容量**
```bash
# ログサイズ確認
du -sh logs/

# ログローテーション設定確認
# docker-compose.yml の logging セクション
```

### エラー別対処法

**Discord Token エラー**
```bash
echo "DISCORD_TOKEN=your_actual_token" > .env
./docker_bot.sh restart
```

**権限エラー**
```bash
sudo chown -R $USER:$USER ./logs
chmod 755 ./logs
```

**ポート競合**
```bash
# 使用中のポート確認
docker ps
netstat -tlnp
```

## 🚀 開発・カスタマイズ

### ローカル開発
```bash
# コンテナ内でデバッグ
./docker_bot.sh shell

# Python仮想環境での開発
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### ソース変更の反映
```bash
# ソースファイル編集後
./docker_bot.sh restart

# requirements.txt変更後
./docker_bot.sh update
```

### 新機能追加
1. `main.py`を編集
2. 必要に応じて`requirements.txt`更新
3. `./docker_bot.sh update`で反映

## 💾 バックアップ・復旧

### バックアップ作成
```bash
# 設定ファイルバックアップ
./docker_bot.sh backup

# 手動バックアップ
tar -czf backup_$(date +%Y%m%d).tar.gz \
  .env docker-compose.yml Dockerfile main.py logs/
```

### 復旧手順
```bash
# バックアップから復旧
tar -xzf backup_20241201.tar.gz
./docker_bot.sh start
```

## 🔒 セキュリティ

### Docker セキュリティ設定
- 非rootユーザーでの実行
- `no-new-privileges` 設定
- 読み取り専用ファイルシステム（部分的）
- リソース制限

### 環境変数保護
- `.env`ファイルはGit管理外
- コンテナ内でのみ環境変数利用
- Dockerイメージにはトークン含まず

## 📈 パフォーマンス

### リソース使用量目安
- **メモリ**: 約30-50MB
- **CPU**: ほぼ0%（待機時）
- **ディスク**: 約100MB（イメージ含む）

### 最適化設定
- ログローテーション: 10MBx3ファイル
- メモリ制限: 128MB
- CPU制限: 0.5コア

---

## 🎉 おわりに

このDiscord Botは治安の悪いサーバー向けに作られた、治安の悪いBotです。  
皆さんの治安の悪い Discord ライフをお楽しみください！  
  
何かあったら適当にissueでも立ててください（投げやり  