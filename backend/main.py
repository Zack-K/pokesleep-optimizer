"""
FastAPIアプリケーションのエントリーポイント
Dockerコンテナ内での実行に対応
"""
import sys
import os

# Pythonパスを設定
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
except ImportError:
    # 代替パスで試行
    import sys
    sys.path.append('/app')
    from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)