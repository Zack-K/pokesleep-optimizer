# ポケモンスリープ最適化アプリケーション Makefile

.PHONY: help build build-optimized build-stable up up-optimized up-stable down logs test lint clean

# デフォルトターゲット
help:
	@echo "利用可能なコマンド:"
	@echo "  build          - 通常のDockerイメージをビルド"
	@echo "  build-optimized - 最適化されたDockerイメージをビルド"
	@echo "  build-stable   - 安定版Dockerイメージをビルド（推奨）"
	@echo "  up             - 通常版でアプリケーションを起動"
	@echo "  up-optimized   - 最適化版でアプリケーションを起動"
	@echo "  up-stable      - 安定版でアプリケーションを起動（推奨）"
	@echo "  down           - アプリケーションを停止"
	@echo "  logs           - ログを表示"
	@echo "  test           - テストを実行"
	@echo "  lint           - コード品質チェック"
	@echo "  clean          - 未使用のイメージとボリュームを削除"
	@echo "  size           - イメージサイズを比較"

# 通常ビルド
build:
	docker compose build

# 最適化ビルド
build-optimized:
	docker compose -f docker-compose.optimized.yml build

# 安定版ビルド（推奨）
build-stable:
	docker compose -f docker-compose.stable.yml build

# 通常起動
up:
	docker compose up -d

# 最適化起動
up-optimized:
	docker compose -f docker-compose.optimized.yml up -d

# 安定版起動（推奨）
up-stable:
	docker compose -f docker-compose.stable.yml up -d

# 停止
down:
	docker compose down
	docker compose -f docker-compose.optimized.yml down
	docker compose -f docker-compose.stable.yml down

# ログ表示
logs:
	docker compose logs -f

# ログ表示（最適化版）
logs-optimized:
	docker compose -f docker-compose.optimized.yml logs -f

# テスト実行
test:
	docker compose exec backend pytest
	docker compose exec frontend npm test

# バックエンドのみテスト
test-backend:
	docker compose exec backend pytest

# フロントエンドのみテスト
test-frontend:
	docker compose exec frontend npm test

# Hadolintでコード品質チェック
lint:
	@echo "Dockerfileのリンティング..."
	@if command -v hadolint >/dev/null 2>&1; then \
		hadolint backend/Dockerfile || true; \
		hadolint backend/Dockerfile.optimized || true; \
		hadolint frontend/Dockerfile || true; \
		hadolint frontend/Dockerfile.optimized || true; \
	else \
		echo "Hadolintがインストールされていません。インストール方法:"; \
		echo "  macOS: brew install hadolint"; \
		echo "  Linux: wget -O hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 && chmod +x hadolint"; \
	fi

# クリーンアップ
clean:
	docker system prune -f
	docker volume prune -f

# イメージサイズ比較
size:
	@echo "=== イメージサイズ比較 ==="
	@echo "通常版:"
	@docker images pokesleep-optimizer-backend:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "通常版バックエンドイメージが見つかりません"
	@docker images pokesleep-optimizer-frontend:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "通常版フロントエンドイメージが見つかりません"
	@echo ""
	@echo "最適化版:"
	@docker images pokesleep-optimizer-backend-optimized:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "最適化版バックエンドイメージが見つかりません"
	@docker images pokesleep-optimizer-frontend-optimized:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "最適化版フロントエンドイメージが見つかりません"

# 開発環境セットアップ（安定版推奨）
setup-dev:
	@echo "開発環境をセットアップしています..."
	make build-stable
	make up-stable
	@echo "セットアップ完了! http://localhost:3000 でアクセスできます"

# 開発環境セットアップ（最適化版）
setup-dev-optimized:
	@echo "最適化版開発環境をセットアップしています..."
	make build-optimized
	make up-optimized
	@echo "セットアップ完了! http://localhost:3000 でアクセスできます"

# 本番環境デプロイ
deploy-prod:
	@echo "本番環境にデプロイしています..."
	make build-optimized
	docker compose -f docker-compose.optimized.yml up -d --scale backend=2
	@echo "デプロイ完了!"

# ベンチマーク
benchmark:
	@echo "パフォーマンステストを実行中..."
	@if command -v ab >/dev/null 2>&1; then \
		ab -n 100 -c 10 http://localhost:8000/health; \
	else \
		echo "Apache Bench (ab) がインストールされていません"; \
	fi