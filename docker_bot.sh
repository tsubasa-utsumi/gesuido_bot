#!/bin/bash

# Gesuido Bot Docker 管理スクリプト
CONTAINER_NAME="gesuido_bot"

case "$1" in
  start)
    echo "🚀 Gesuido Bot を起動します..."
    docker-compose up -d
    echo "✅ Bot起動完了"
    ;;
    
  stop)
    echo "🛑 Gesuido Bot を停止します..."
    docker-compose down
    echo "✅ Bot停止完了"
    ;;
    
  restart)
    echo "🔄 Gesuido Bot を再起動します..."
    docker-compose restart
    echo "✅ Bot再起動完了"
    ;;
    
  status)
    echo "📊 Gesuido Bot ステータス確認"
    echo "=============================="
    
    # コンテナ状態確認
    echo "🔍 コンテナ状態:"
    docker-compose ps
    
    echo ""
    echo "💾 リソース使用量:"
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
      docker stats $CONTAINER_NAME --no-stream
    else
      echo "❌ コンテナが実行されていません"
    fi
    
    echo ""
    echo "🏥 ヘルスチェック:"
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
      HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME 2>/dev/null || echo "no-healthcheck")
      echo "状態: $HEALTH"
    else
      echo "❌ コンテナが実行されていません"
    fi
    ;;
    
  logs)
    echo "📝 Gesuido Bot ログ表示"
    if [ "$2" = "-f" ] || [ "$2" = "--follow" ]; then
      echo "リアルタイムログ監視中... (Ctrl+C で終了)"
      docker-compose logs -f
    else
      echo "最新ログ表示:"
      docker-compose logs --tail=50
    fi
    ;;
    
  shell)
    echo "🐚 コンテナにシェル接続..."
    docker-compose exec gesuido_bot /bin/bash
    ;;
    
  update)
    echo "🔄 Bot更新 (ソース変更後の再起動)"
    echo "1. イメージ再ビルド中..."
    docker-compose build
    echo "2. コンテナ再起動中..."
    docker-compose up -d
    echo "✅ 更新完了"
    ;;
    
  clean)
    echo "🧹 Docker リソース クリーンアップ"
    echo "停止中のコンテナ、未使用のイメージ等を削除します"
    read -p "実行しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      docker-compose down
      docker system prune -f
      echo "✅ クリーンアップ完了"
    else
      echo "キャンセルしました"
    fi
    ;;
    
  backup)
    echo "💾 設定ファイルバックアップ作成中..."
    BACKUP_NAME="gesuido_bot_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$BACKUP_NAME" \
      .env \
      docker-compose.yml \
      Dockerfile \
      main.py \
      requirements.txt \
      logs/ 2>/dev/null || true
    echo "✅ バックアップ作成: $BACKUP_NAME"
    ;;
    
  *)
    echo "🤖 Gesuido Bot Docker 管理スクリプト"
    echo ""
    echo "使用方法: $0 {command}"
    echo ""
    echo "利用可能なコマンド:"
    echo "  start      - Bot起動"
    echo "  stop       - Bot停止"
    echo "  restart    - Bot再起動"
    echo "  status     - 状態確認"
    echo "  logs [-f]  - ログ表示 (-f でリアルタイム)"
    echo "  shell      - コンテナにシェル接続"
    echo "  update     - ソース変更後の更新"
    echo "  clean      - Dockerリソースクリーンアップ"
    echo "  backup     - 設定ファイルバックアップ"
    echo ""
    echo "例:"
    echo "  $0 start         # Bot起動"
    echo "  $0 logs -f       # リアルタイムログ"
    echo "  $0 status        # ステータス確認"
    exit 1
    ;;
esac