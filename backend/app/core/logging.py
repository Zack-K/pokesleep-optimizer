"""
ログ設定
FastAPI ベストプラクティスに従ったログ設定
"""
import logging
import sys
from typing import Dict, Any
from .config import settings


class ColoredFormatter(logging.Formatter):
    """カラー付きログフォーマッター"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # レコードのコピーを作成してカラー情報を追加
        colored_record = logging.makeLogRecord(record.__dict__)
        colored_record.levelname = f"{log_color}{record.levelname}{reset_color}"
        
        return super().format(colored_record)


def setup_logging() -> None:
    """ログ設定のセットアップ"""
    
    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # 既存のハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))
    
    # フォーマッター（開発環境ではカラー付き）
    if settings.debug:
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 外部ライブラリのログレベル調整
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # アプリケーションロガー
    app_logger = logging.getLogger("app")
    app_logger.setLevel(getattr(logging, settings.log_level))


def get_logger(name: str) -> logging.Logger:
    """名前付きロガーの取得"""
    return logging.getLogger(f"app.{name}")


class LoggingMixin:
    """ログ機能ミックスイン"""
    
    @property
    def logger(self) -> logging.Logger:
        """クラス専用のロガーを取得"""
        return get_logger(self.__class__.__name__)


# ログレベル定数
LOG_LEVELS: Dict[str, int] = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}