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
from ...services.genetic_optimizer import GeneticOptimizer
from ...services.multi_objective_optimizer import MultiObjectiveOptimizer, OptimizationObjectives
from ...services.performance_optimizer import BenchmarkRunner, OptimizationCache
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
    "/optimizable-names",
    response_model=List[str],
    summary="最適化可能ポケモン名一覧取得",
    description="最適化可能なポケモン名の一覧を取得します"
)
async def get_optimizable_pokemon_names(
    data_manager=Depends(get_pokemon_data_manager)
):
    """最適化可能ポケモン名一覧の取得"""
    try:
        names = data_manager.get_optimizable_pokemon_names()
        return names
    except Exception as e:
        logger.error(f"Failed to get optimizable pokemon names: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="最適化可能ポケモン名一覧の取得に失敗しました"
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
        
        # 最終週の結果から食材・レシピデータを取得
        simulation = result["simulation_result"]
        final_week = simulation["weekly_results"][-1] if simulation["weekly_results"] else {}
        ingredients_data = final_week.get("ingredients_remaining", {})
        recipes_data = final_week.get("recipes", {})
        
        return {
            "party_names": result["best_party"],
            "total_energy": result["best_energy"],
            "daily_energy": result["best_energy"] / (request.weeks_to_simulate * 7),
            "recipe_energy": simulation["averages"]["recipe_energy"],
            "ingredients": ingredients_data,
            "recipes_made": recipes_data,
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
        
        # 最終週の結果から食材・レシピデータを取得
        final_week = simulation["weekly_results"][-1] if simulation["weekly_results"] else {}
        ingredients_data = final_week.get("ingredients_remaining", {})
        recipes_data = final_week.get("recipes", {})
        
        return {
            "party_names": result["party_names"],
            "total_energy": simulation["averages"]["total_energy"],
            "daily_energy": simulation["averages"]["daily_energy"],
            "recipe_energy": simulation["averages"]["recipe_energy"],
            "berry_energy": simulation["averages"]["berry_energy"],
            "ingredients": ingredients_data,
            "recipes_made": recipes_data,
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


@router.post(
    "/optimize-genetic",
    response_model=Dict[str, Any],
    summary="遺伝的アルゴリズム最適化",
    description="遺伝的アルゴリズムを使用して最適なパーティ構成を探索します"
)
async def optimize_party_genetic(
    request: OptimizationRequest,
    data_manager=Depends(get_pokemon_data_manager)
):
    """遺伝的アルゴリズムによる最適化"""
    try:
        available_pokemon = data_manager.get_optimizable_pokemon_names()
        
        optimizer = GeneticOptimizer(
            available_pokemon=available_pokemon,
            population_size=50,
            elite_size=10,
            mutation_rate=0.1,
            max_generations=100
        )
        
        result = optimizer.optimize(
            must_include=request.must_include,
            field_bonus=request.field_settings.field_bonus,
            pot_capacity=request.field_settings.pot_capacity,
            recipe_requests=["カレー"],
            weeks_to_simulate=request.weeks_to_simulate
        )
        
        # シミュレーション結果の詳細取得
        detailed_result = optimization_service.evaluate_specific_party(
            party_names=result["best_individual"],
            field_bonus=request.field_settings.field_bonus,
            pot_capacity=request.field_settings.pot_capacity,
            recipe_requests=["カレー"],
            weeks_to_simulate=request.weeks_to_simulate
        )
        
        simulation = detailed_result["simulation_result"]
        
        return {
            "optimization_method": "genetic_algorithm",
            "party_names": result["best_individual"],
            "fitness": result["best_fitness"],
            "total_energy": simulation["averages"]["total_energy"],
            "daily_energy": simulation["averages"]["daily_energy"],
            "recipe_energy": simulation["averages"]["recipe_energy"],
            "berry_energy": simulation["averages"]["berry_energy"],
            "ingredients": simulation["weekly_results"][-1]["ingredients_remaining"] if simulation["weekly_results"] else {},
            "recipes_made": simulation["weekly_results"][-1]["recipes"] if simulation["weekly_results"] else {},
            "generations_completed": result["generations_completed"],
            "convergence_history": result["convergence_history"],
            "population_stats": result["final_population_stats"],
            "weekly_results": simulation["weekly_results"]
        }
        
    except Exception as e:
        logger.error(f"Genetic optimization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"遺伝的アルゴリズム最適化に失敗しました: {e}"
        )


@router.post(
    "/optimize-multi-objective",
    response_model=Dict[str, Any],
    summary="マルチ目的最適化",
    description="複数の目的関数を同時に最適化してパレート最適解を探索します"
)
async def optimize_party_multi_objective(
    request: OptimizationRequest,
    optimization_type: str = "balanced",  # balanced, energy_focused, recipe_focused
    data_manager=Depends(get_pokemon_data_manager)
):
    """マルチ目的最適化"""
    try:
        available_pokemon = data_manager.get_optimizable_pokemon_names()
        
        # 最適化目的の選択
        if optimization_type == "balanced":
            objectives = OptimizationObjectives.create_balanced()
        elif optimization_type == "energy_focused":
            objectives = OptimizationObjectives.create_energy_focused()
        elif optimization_type == "recipe_focused":
            objectives = OptimizationObjectives.create_recipe_focused()
        else:
            objectives = OptimizationObjectives.create_comprehensive()
        
        optimizer = MultiObjectiveOptimizer(
            objectives=objectives,
            population_size=50,
            max_generations=50
        )
        
        result = optimizer.optimize(
            available_pokemon=available_pokemon,
            must_include=request.must_include,
            field_bonus=request.field_settings.field_bonus,
            pot_capacity=request.field_settings.pot_capacity,
            recipe_requests=["カレー", "サラダ", "デザート"],
            weeks_to_simulate=request.weeks_to_simulate
        )
        
        # 最適解の詳細シミュレーション
        best_party = result["best_compromise"]["party"]
        detailed_result = optimization_service.evaluate_specific_party(
            party_names=best_party,
            field_bonus=request.field_settings.field_bonus,
            pot_capacity=request.field_settings.pot_capacity,
            recipe_requests=["カレー", "サラダ", "デザート"],
            weeks_to_simulate=request.weeks_to_simulate
        )
        
        simulation = detailed_result["simulation_result"]
        
        return {
            "optimization_method": "multi_objective",
            "optimization_type": optimization_type,
            "pareto_front": result["pareto_front"],
            "best_compromise": result["best_compromise"],
            "objective_names": result["objective_names"],
            "generations_completed": result["generations_completed"],
            "party_names": best_party,
            "objectives": result["best_compromise"]["objectives"],
            "total_energy": simulation["averages"]["total_energy"],
            "daily_energy": simulation["averages"]["daily_energy"],
            "recipe_energy": simulation["averages"]["recipe_energy"],
            "berry_energy": simulation["averages"]["berry_energy"],
            "ingredients": simulation["weekly_results"][-1]["ingredients_remaining"] if simulation["weekly_results"] else {},
            "recipes_made": simulation["weekly_results"][-1]["recipes"] if simulation["weekly_results"] else {},
            "weekly_results": simulation["weekly_results"]
        }
        
    except Exception as e:
        logger.error(f"Multi-objective optimization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"マルチ目的最適化に失敗しました: {e}"
        )


@router.post(
    "/benchmark",
    response_model=Dict[str, Any],
    summary="最適化手法ベンチマーク",
    description="複数の最適化手法のパフォーマンスを比較します"
)
async def benchmark_optimization_methods(
    request: OptimizationRequest,
    methods: List[str] = ["brute_force", "genetic", "multi_objective"],
    runs_per_method: int = 3,
    data_manager=Depends(get_pokemon_data_manager)
):
    """最適化手法のベンチマーク"""
    try:
        available_pokemon = data_manager.get_optimizable_pokemon_names()
        
        def run_optimization(method: str, **kwargs) -> Dict[str, Any]:
            """最適化実行関数"""
            if method == "brute_force":
                return optimization_service.find_optimal_party(
                    must_include=request.must_include,
                    field_bonus=request.field_settings.field_bonus,
                    pot_capacity=request.field_settings.pot_capacity,
                    recipe_requests=["カレー"],
                    weeks_to_simulate=request.weeks_to_simulate,
                    max_combinations=1000  # ベンチマーク用に制限
                )
            elif method == "genetic":
                optimizer = GeneticOptimizer(
                    available_pokemon=available_pokemon,
                    population_size=20,  # ベンチマーク用に小さく
                    max_generations=20
                )
                return optimizer.optimize(
                    must_include=request.must_include,
                    field_bonus=request.field_settings.field_bonus,
                    pot_capacity=request.field_settings.pot_capacity,
                    recipe_requests=["カレー"],
                    weeks_to_simulate=request.weeks_to_simulate
                )
            elif method == "multi_objective":
                objectives = OptimizationObjectives.create_balanced()
                optimizer = MultiObjectiveOptimizer(
                    objectives=objectives,
                    population_size=20,
                    max_generations=20
                )
                return optimizer.optimize(
                    available_pokemon=available_pokemon,
                    must_include=request.must_include,
                    field_bonus=request.field_settings.field_bonus,
                    pot_capacity=request.field_settings.pot_capacity,
                    recipe_requests=["カレー"],
                    weeks_to_simulate=request.weeks_to_simulate
                )
            else:
                raise ValueError(f"Unknown optimization method: {method}")
        
        # ベンチマーク実行
        runner = BenchmarkRunner()
        benchmark_results = runner.run_optimization_benchmark(
            optimizer_function=run_optimization,
            methods=methods,
            test_params={},
            runs_per_method=runs_per_method
        )
        
        # パフォーマンスレポート生成
        performance_report = runner.generate_performance_report(benchmark_results)
        
        return {
            "benchmark_results": benchmark_results,
            "performance_report": performance_report,
            "test_parameters": {
                "methods": methods,
                "runs_per_method": runs_per_method,
                "must_include": request.must_include,
                "field_settings": request.field_settings.dict(),
                "weeks_to_simulate": request.weeks_to_simulate
            }
        }
        
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ベンチマーク実行に失敗しました: {e}"
        )