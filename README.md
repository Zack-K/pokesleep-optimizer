# ポケモンスリープ 1週間最適パーティ編成計算アプリケーション

## 概要
ポケモンスリープにおいて、1週間のパフォーマンスを最大化するための最適なパーティ編成を計算するWebアプリケーションです。

## 技術スタック
- **バックエンド**: FastAPI + Python
- **フロントエンド**: React + TypeScript + Material-UI
- **コンテナ**: Docker + Docker Compose

## 機能
- ポケモンデータベース管理
- パーティ編成最適化計算
- 1週間シミュレーション
- 結果の可視化とダッシュボード

## セットアップ

### 前提条件
- Docker
- Docker Compose
- Make (オプション、便利なコマンド実行用)

### 起動方法

#### 簡単セットアップ（推奨）
```bash
# プロジェクトディレクトリに移動
cd pokesleep-optimizer

# 最適化版で起動（軽量・高速）
make setup-dev
```

#### 手動セットアップ
```bash
# 最適化版でビルド・起動
docker compose -f docker-compose.optimized.yml up --build

# または通常版
docker compose up --build
```

### アクセス
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API文書: http://localhost:8000/docs

### Docker最適化

#### 最適化の効果
- **軽量ベースイメージ**: Alpine Linux使用で大幅なサイズ削減
- **マルチステージビルド**: 不要なビルドツールを最終イメージから除外
- **レイヤー最適化**: キャッシュ効率を最大化
- **セキュリティ強化**: 非rootユーザーでの実行
- **リソース制限**: メモリとCPU使用量を制御

#### サイズ比較
```bash
# イメージサイズを比較
make size
```

#### 利用可能なコマンド
```bash
# 全コマンド一覧
make help

# 最適化版の起動
make up-optimized

# ログ表示
make logs-optimized

# テスト実行
make test

# コード品質チェック
make lint
```

## 開発

### バックエンド開発
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### フロントエンド開発
```bash
cd frontend
npm install
npm start
```

## テスト

### バックエンドテスト
```bash
cd backend
pytest
```

### フロントエンドテスト
```bash
cd frontend
npm test
```