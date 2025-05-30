# Railway デプロイ詳細ガイド

## 1. Railway登録
1. https://railway.app にアクセス
2. 「Start a New Project」をクリック
3. 「Login with GitHub」を選択
4. GitHubの認証画面で「Authorize Railway」をクリック

## 2. プロジェクト作成
1. Railwayダッシュボードで「New Project」をクリック
2. 「Deploy from GitHub repo」を選択
3. 先ほど作成したDiscord Botリポジトリを選択
4. 「Deploy Now」をクリック

## 3. 環境変数の設定
1. デプロイされたサービスをクリック
2. 「Variables」タブをクリック
3. 「New Variable」をクリック
4. 以下を設定:
   - Name: `DISCORD_TOKEN`
   - Value: あなたのDiscord Botトークン

## 4. サービス設定の確認
1. 「Settings」タブで以下を確認:
   - Build Command: (空白でOK、requirements.txtから自動判定)
   - Start Command: `python main.py` (Procfileがあれば自動設定)

## 5. デプロイの確認
1. 「Deployments」タブでビルド状況を確認
2. 「Logs」タブでBotの起動ログを確認
3. 「Bot がログインしました！」が表示されれば成功

## 6. 自動再デプロイ設定
- GitHubにプッシュすると自動的に再デプロイされます
- 設定変更は不要です

## トラブルシューティング
- ログで「DISCORD_TOKENが設定されていません」→環境変数を確認
- ログで権限エラー→Discord Developer PortalでBot権限を確認
- デプロイ失敗→requirements.txtとProcfileを確認