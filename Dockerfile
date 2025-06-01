# Gesuido Bot Dockerfile
FROM python:3.12-slim

# 作業ディレクトリ設定
WORKDIR /app

# システムパッケージ更新とタイムゾーン設定
RUN apt-get update && apt-get install -y \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# タイムゾーンを日本時間に設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Python依存関係ファイルをコピー
COPY requirements.txt .

# Python依存関係インストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 出力バッファリングを無効化（ログの即座表示）
ENV PYTHONUNBUFFERED=1

# ログディレクトリ作成
RUN mkdir -p /var/log/gesuido_bot

# 非rootユーザー作成（セキュリティ向上）
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app /var/log/gesuido_bot
USER botuser

# ソースコードはマウントで提供されるため、ここではコピーしない
# ポート公開（必要に応じて）
# EXPOSE 8080

# 起動コマンド
CMD ["python", "main.py"]