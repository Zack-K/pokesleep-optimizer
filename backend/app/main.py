"""
FastAPI メインアプリケーション
ベストプラクティスに従った統合実装
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time

from .core.config import settings
from .core.logging import setup_logging
from .api.v1.pokemon import router as pokemon_router
from .models.schemas import ErrorResponse

# ログ設定の初期化
setup_logging()
logger = logging.getLogger("app.main")

# FastAPIアプリケーション作成
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# ミドルウェア: リクエスト処理時間ログ
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """リクエスト処理時間のログ記録"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 例外ハンドラー
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP例外ハンドラー"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP_ERROR",
            message=str(exc.detail),
            details={"status_code": exc.status_code, "url": str(request.url)}
        ).dict()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """バリデーションエラーハンドラー"""
    logger.error(f"Validation error: {exc.errors()} - {request.url}")
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="VALIDATION_ERROR",
            message="リクエストデータが不正です",
            details={"errors": exc.errors(), "url": str(request.url)}
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """一般例外ハンドラー"""
    logger.error(f"Unexpected error: {exc} - {request.url}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="内部サーバーエラーが発生しました",
            details={"url": str(request.url)}
        ).dict()
    )


# ルーター登録
app.include_router(pokemon_router, prefix="/api/v1")


# ルートエンドポイント
@app.get("/", summary="API情報", description="API基本情報を取得します")
async def root():
    """ルートエンドポイント"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs_url": "/docs",
        "health_check": "/api/v1/pokemon/health"
    }


@app.get(
    "/health",
    summary="ヘルスチェック",
    description="アプリケーション全体の稼働状況を確認します"
)
async def health_check():
    """アプリケーション全体のヘルスチェック"""
    try:
        from .data.pokemon_data import pokemon_data_manager
        
        pokemon_count = pokemon_data_manager.get_pokemon_count()
        load_status = pokemon_data_manager.get_load_status()
        
        return {
            "status": "healthy" if load_status and pokemon_count > 0 else "unhealthy",
            "version": settings.app_version,
            "pokemon_loaded": pokemon_count,
            "data_load_status": load_status,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "version": settings.app_version,
            "error": str(e),
            "timestamp": time.time()
        }


# 起動イベント
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Allowed origins: {settings.allowed_origins}")
    
    # データ初期化確認
    try:
        from .data.pokemon_data import pokemon_data_manager
        pokemon_count = pokemon_data_manager.get_pokemon_count()
        logger.info(f"Pokemon data loaded: {pokemon_count} pokemon available")
        
        if pokemon_count == 0:
            logger.warning("No pokemon data loaded")
        
    except Exception as e:
        logger.error(f"Failed to initialize pokemon data: {e}")


# 終了イベント
@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
        reload=settings.debug
    )