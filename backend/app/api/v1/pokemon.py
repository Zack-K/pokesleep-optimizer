"""
Pokemon API ルーター
FastAPIのベストプラクティスに従った依存性注入パターンの実装
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from ...models.schemas import (
    PokemonInfo,
    OptimizationRequest,
    SimulationResult,
    ErrorResponse,
    HealthResponse
)
from ...services.simulation_service import optimization_service
from ...data.pokemon_data import pokemon_data_manager
from ...core.config import settings

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


def get_optimization_service():
    """依存性注入: 最適化サービス"""
    return optimization_service


def get_pokemon_data_manager():
    """依存性注入: ポケモンデータマネージャー"""
    return pokemon_data_manager


@router.get(
    "/",
    response_model=List[Dict[str, Any]],
    summary="全ポケモン情報取得",
    description="利用可能な全ポケモンの基本情報を取得します"
)
async def get_all_pokemon(
    data_manager=Depends(get_pokemon_data_manager)
):
    """全ポケモン情報の取得"""
    try:
        pokemon_list = data_manager.get_all_pokemon_info()
        return pokemon_list
    except Exception as e:
        logger.error(f"Failed to get pokemon list: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ポケモン情報の取得に失敗しました"
        )


@router.get(
    "/names",
    response_model=List[str],
    summary="ポケモン名一覧取得",
    description="利用可能なポケモン名の一覧を取得します"
)
async def get_pokemon_names(
    data_manager=Depends(get_pokemon_data_manager)
):
    """ポケモン名一覧の取得"""
    try:
        names = data_manager.get_available_pokemon_names()
        return names
    except Exception as e:
        logger.error(f"Failed to get pokemon names: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ポケモン名一覧の取得に失敗しました"
        )


@router.get(
    "/{pokemon_name}",
    response_model=Dict[str, Any],
    summary="個別ポケモン情報取得",
    description="指定されたポケモンの詳細情報を取得します"
)
async def get_pokemon_info(
    pokemon_name: str,
    data_manager=Depends(get_pokemon_data_manager)
):
    """個別ポケモン情報の取得"""
    try:
        if not data_manager.is_valid_pokemon_name(pokemon_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ポケモン '{pokemon_name}' が見つかりません"
            )
        
        pokemon_info = data_manager.get_pokemon_base_info(pokemon_name)
        return pokemon_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get pokemon info for {pokemon_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ポケモン情報の取得に失敗しました"
        )


@router.get(
    "/type/{pokemon_type}",
    response_model=List[str],
    summary="タイプ別ポケモン取得",
    description="指定されたタイプのポケモン一覧を取得します"
)
async def get_pokemon_by_type(
    pokemon_type: str,
    data_manager=Depends(get_pokemon_data_manager)
):
    """タイプ別ポケモンの取得"""
    try:
        valid_types = ["きのみ", "食材", "スキル"]
        if pokemon_type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"無効なポケモンタイプ: {pokemon_type}. 有効なタイプ: {valid_types}"
            )
        
        pokemon_names = data_manager.get_pokemon_by_type(pokemon_type)
        return pokemon_names
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get pokemon by type {pokemon_type}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="タイプ別ポケモンの取得に失敗しました"
        )


@router.post(
    "/validate-party",
    response_model=Dict[str, Any],
    summary="パーティ構成検証",
    description="パーティ構成の妥当性をチェックします"
)
async def validate_party(
    party_names: List[str],
    data_manager=Depends(get_pokemon_data_manager)
):
    """パーティ構成の検証"""
    try:
        validation_result = data_manager.validate_party_composition(party_names)
        return validation_result
    except Exception as e:
        logger.error(f"Failed to validate party {party_names}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="パーティ構成の検証に失敗しました"
        )


@router.post(
    "/optimize",
    response_model=Dict[str, Any],
    summary="最適パーティ探索",
    description="指定された条件で最適なパーティ構成を探索します"
)
async def optimize_party(
    request: OptimizationRequest,
    service=Depends(get_optimization_service)
):
    """最適パーティの探索"""
    try:
        result = service.find_optimal_party(
            must_include=request.must_include,
            field_bonus=request.field_settings.field_bonus,
            pot_capacity=request.field_settings.pot_capacity,
            recipe_requests=["カレー"],  # TODO: レシピタイプ対応
            weeks_to_simulate=request.weeks_to_simulate,
            max_combinations=1000
        )
        
        return {
            "party_names": result["best_party"],
            "total_energy": result["best_energy"],
            "daily_energy": result["best_energy"] / (request.weeks_to_simulate * 7),
            "recipe_energy": result["simulation_result"]["averages"]["recipe_energy"],
            "ingredients": {},  # TODO: 詳細食材情報
            "recipes_made": [],  # TODO: レシピ情報
            "optimization_stats": result["optimization_stats"]
        }
        
    except ValueError as e:
        logger.warning(f"Invalid optimization request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to optimize party: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="パーティ最適化に失敗しました"
        )


@router.post(
    "/evaluate",
    response_model=Dict[str, Any],
    summary="特定パーティ評価",
    description="指定されたパーティ構成のパフォーマンスを評価します"
)
async def evaluate_party(
    party_names: List[str],
    field_bonus: float = 1.57,
    pot_capacity: int = 69,
    weeks_to_simulate: int = 3,
    service=Depends(get_optimization_service)
):
    """特定パーティの評価"""
    try:
        result = service.evaluate_specific_party(
            party_names=party_names,
            field_bonus=field_bonus,
            pot_capacity=pot_capacity,
            recipe_requests=["カレー"],
            weeks_to_simulate=weeks_to_simulate
        )
        
        simulation = result["simulation_result"]
        
        return {
            "party_names": result["party_names"],
            "total_energy": simulation["averages"]["total_energy"],
            "daily_energy": simulation["averages"]["daily_energy"],
            "recipe_energy": simulation["averages"]["recipe_energy"],
            "berry_energy": simulation["averages"]["berry_energy"],
            "ingredients": {},  # TODO: 詳細食材情報
            "recipes_made": [],  # TODO: レシピ情報
            "validation": result["validation"],
            "weekly_results": simulation["weekly_results"]
        }
        
    except ValueError as e:
        logger.warning(f"Invalid party evaluation request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to evaluate party: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="パーティ評価に失敗しました"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="ヘルスチェック",
    description="Pokemon APIの稼働状況とデータ読み込み状況を確認します"
)
async def health_check(
    data_manager=Depends(get_pokemon_data_manager)
):
    """ヘルスチェック"""
    try:
        pokemon_count = data_manager.get_pokemon_count()
        load_status = data_manager.get_load_status()
        
        status_text = "healthy" if load_status and pokemon_count > 0 else "unhealthy"
        
        return HealthResponse(
            status=status_text,
            pokemon_count=pokemon_count,
            version=settings.app_version
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            pokemon_count=0,
            version=settings.app_version
        )