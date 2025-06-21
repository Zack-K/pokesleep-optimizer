# ポケモンスリープ 最適パーティ編成計算アプリケーション

## 概要
ポケモンスリープにおいて、エナジー効率を最大化するための最適なパーティ編成を計算するWebアプリケーションです。複数の最適化アルゴリズムを提供し、詳細なシミュレーション結果と可視化機能を備えています。

## 技術スタック
- **バックエンド**: FastAPI + Python 3.11
- **フロントエンド**: React 18 + TypeScript + Material-UI v5
- **コンテナ**: Docker + Docker Compose (Alpine Linux ベース)
- **最適化**: 遺伝的アルゴリズム、マルチ目的最適化、総当たり

## 主要機能

### 🎯 パーティ最適化
- **遺伝的アルゴリズム**: 効率的な探索で高品質な解を発見
- **マルチ目的最適化**: 複数の目標を同時に最適化（パレート最適解）
- **総当たり**: 全組み合わせの評価（小規模パーティ向け）
- **ベンチマーク**: 複数手法のパフォーマンス比較

### 📊 シミュレーション機能  
- **3週間シミュレーション**: 詳細なエナジー計算
- **獲得食材分析**: 種類別生産量と構成比
- **レシピ作成計算**: 食材からレシピへの変換
- **リアルタイム結果表示**: 最適化進捗の可視化

### 📈 データ可視化
- **エナジー統計**: 総エナジー、日平均、レシピエナジー
- **食材チャート**: 棒グラフと円グラフによる視覚化
- **パフォーマンス比較**: ベンチマーク結果の表形式表示
- **レスポンシブデザイン**: モバイル対応UI

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
- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API文書**: http://localhost:8000/docs

## 使用方法

### 基本的な使い方

1. **ポケモン選択**
   - 「ポケモン一覧」タブで最大5匹まで選択
   - タイプ別フィルタリング機能を活用

2. **最適化実行**
   - 「パーティ最適化」タブに移動
   - フィールドボーナス（1.0-2.0）と鍋容量を設定
   - 最適化手法を選択：
     - **遺伝的アルゴリズム**: バランス重視、高速
     - **マルチ目的最適化**: 複数目標の同時最適化
     - **総当たり**: 完全探索（小規模向け）

3. **結果確認**
   - 「シミュレーション結果」タブで詳細データを確認
   - エナジー統計、獲得食材、レシピ情報を可視化

### 高度な機能

#### ベンチマーク実行
複数の最適化手法を比較し、パフォーマンス分析を実施
```
実行時間、成功率、相対速度の比較表示
```

#### 最適化パラメータ
- **フィールドボーナス**: 1.57（デフォルト）
- **鍋容量**: 69（デフォルト）  
- **シミュレーション期間**: 3週間（21日間）

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

## トラブルシューティング

### よくある問題

#### コンテナ起動時のエラー
```bash
# コンテナを完全に再構築
docker compose -f docker-compose.optimized.yml down
docker compose -f docker-compose.optimized.yml up --build

# イメージとボリュームのクリア
docker system prune -a
```

#### フロントエンドが表示されない
- ブラウザのキャッシュをクリア
- http://localhost:3000 でアクセス確認
- バックエンドAPIの状態確認: http://localhost:8000/health

#### 最適化計算がエラーになる
- ポケモンが正しく選択されているか確認
- パーティサイズ（1-5匹）の範囲内か確認
- ブラウザのデベロッパーツールでエラーログ確認

### パフォーマンス最適化

#### メモリ使用量削減
```bash
# 軽量版の使用
docker compose -f docker-compose.optimized.yml up

# 不要なイメージの削除
docker image prune
```

#### 計算速度向上
- 遺伝的アルゴリズムを推奨（総当たりより高速）
- パーティサイズを小さく設定
- ベンチマーク実行時は実行回数を調整

## 技術仕様

### アーキテクチャ
```
Frontend (React) ↔ Backend (FastAPI) ↔ Pokemon Data
     ↓                    ↓                 ↓
  Material-UI        Optimization      JSON Database
     ↓               Algorithms           ↓
  Recharts              ↓            Game Mechanics
     ↓              Simulation            ↓
   Nginx             Service          Energy Calc
```

### API エンドポイント
- `GET /api/v1/pokemon/` - 全ポケモン取得
- `POST /api/v1/pokemon/evaluate` - パーティ評価
- `POST /api/v1/pokemon/optimize-genetic` - 遺伝的アルゴリズム
- `POST /api/v1/pokemon/optimize-multi-objective` - マルチ目的最適化
- `POST /api/v1/pokemon/benchmark` - ベンチマーク実行

### データ形式
```typescript
interface SimulationResult {
  party_names: string[];
  total_energy: number;
  daily_energy: number;
  recipe_energy: number;
  ingredients: Record<string, number>;
  recipes_made: Record<string, any>;
}
```