"""
アプリケーション設定
Pydantic Settingsを使用したベストプラクティス実装
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # アプリケーション基本情報
    app_name: str = "ポケモンスリープ最適化API"
    app_version: str = "1.0.0"
    app_description: str = "1週間の最適パーティ編成を計算するAPI"
    
    # サーバー設定
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS設定
    allowed_origins: List[str] = [
        "http://localhost:3000",  # ローカル開発環境
        "http://frontend:3000",   # Docker環境
        "http://127.0.0.1:3000"   # ローカルIP
    ]
    
    # ログ設定
    log_level: str = "INFO"
    
    # ゲーム設定
    default_field_bonus: float = 1.57
    default_pot_capacity: int = 69
    max_party_size: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()