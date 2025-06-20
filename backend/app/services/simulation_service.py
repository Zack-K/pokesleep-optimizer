"""
シミュレーションサービス
ビジネスロジックの分離とFastAPIベストプラクティスの実装
"""
from typing import List, Dict, Tuple, Any, Optional
import logging
import math
from itertools import combinations
from ..models.pokemon import Pokemon
from ..data.pokemon_data import pokemon_data_manager
from ..core.constants import (
    BERRY, FOOD, ID_RECIPE_CURRY, ID_RECIPE_SALAD, ID_RECIPE_DEZERT,
    COOKING_SUCCESSFUL_RATE, COOKING_SUCCESSFUL_FACT,
    EVENT_BONUS_RECIPE_FACT, RECIPE_LV_BONUS_TABLE
)

logger = logging.getLogger(__name__)


class RecipeCalculator:
    """レシピ計算機"""
    
    def __init__(self):
        """レシピデータの初期化"""
        self.recipes = {
            "カレー": {
                "id": ID_RECIPE_CURRY,
                "base_energy": 2387,
                "ingredients": ["ジンジャー", "トマト", "ミート"],
                "required": [7, 8, 8]
            },
            "サラダ": {
                "id": ID_RECIPE_SALAD,
                "base_energy": 1815,
                "ingredients": ["オイル", "トマト", "ミート"],
                "required": [8, 8, 8]  
            },
            "デザート": {
                "id": ID_RECIPE_DEZERT,
                "base_energy": 1684,
                "ingredients": ["ミルク", "エッグ", "リンゴ"],
                "required": [7, 4, 8]
            }
        }
    
    def calculate_recipe_energy(
        self,
        recipe_name: str,
        ingredients_available: Dict[str, int],
        recipe_level: int = 1,
        pot_capacity: int = 69
    ) -> Dict[str, Any]:
        """レシピエナジーの計算"""
        if recipe_name not in self.recipes:
            return {"energy": 0, "count": 0, "ingredients_used": {}}
        
        recipe = self.recipes[recipe_name]
        required = recipe["required"]
        recipe_ingredients = recipe["ingredients"]
        
        # 各食材の必要数をチェック
        max_recipes = float('inf')
        for i, ingredient in enumerate(recipe_ingredients):
            available = ingredients_available.get(ingredient, 0)
            needed = required[i]
            possible_recipes = available // needed if needed > 0 else 0
            max_recipes = min(max_recipes, possible_recipes)
        
        # 鍋容量による制限
        max_recipes = min(max_recipes, pot_capacity)
        max_recipes = max(0, int(max_recipes))
        
        # レシピレベルボーナス
        level_bonus = 1.0
        if 0 <= recipe_level - 1 < len(RECIPE_LV_BONUS_TABLE):
            level_bonus = 1.0 + RECIPE_LV_BONUS_TABLE[recipe_level - 1]
        
        # エナジー計算
        base_energy = recipe["base_energy"]
        total_energy = base_energy * max_recipes * level_bonus * EVENT_BONUS_RECIPE_FACT
        
        # 使用した食材
        ingredients_used = {}
        for i, ingredient in enumerate(recipe_ingredients):
            ingredients_used[ingredient] = required[i] * max_recipes
        
        return {
            "energy": total_energy,
            "count": max_recipes,
            "ingredients_used": ingredients_used,
            "recipe_level": recipe_level,
            "level_bonus": level_bonus
        }


class PartySimulator:
    """パーティシミュレーター"""
    
    def __init__(self):
        """シミュレーターの初期化"""
        self.recipe_calculator = RecipeCalculator()
    
    def simulate_daily_production(
        self,
        party: List[Pokemon],
        field_bonus: float = 1.57,
        hours: float = 24.0
    ) -> Dict[str, Any]:
        """1日の生産量をシミュレート"""
        total_berry_energy = 0.0
        total_ingredients = {}
        total_skill_triggers = 0.0
        
        party_details = []
        
        for pokemon in party:
            # おてつだい回数の計算
            helps = pokemon.calculate_help_amount(hours)
            
            # きのみエナジー
            berry_energy = helps["berry"] * pokemon.berry_energy * field_bonus
            total_berry_energy += berry_energy
            
            # 食材獲得
            avg_ingredient_per_help = 1.0  # 1回のおてつだいで平均1個
            ingredient_count = helps["ingredient"] * avg_ingredient_per_help
            
            # 各食材を均等に獲得と仮定
            for ingredient in pokemon.ingredients:
                count = ingredient_count / len(pokemon.ingredients)
                total_ingredients[ingredient] = total_ingredients.get(ingredient, 0) + count
            
            # スキル発動回数
            total_skill_triggers += helps["skill"]
            
            party_details.append({
                "name": pokemon.name,
                "helps": helps,
                "berry_energy": berry_energy,
                "ingredients_produced": {
                    ing: ingredient_count / len(pokemon.ingredients) 
                    for ing in pokemon.ingredients
                }
            })
        
        return {
            "total_berry_energy": total_berry_energy,
            "total_ingredients": total_ingredients,
            "total_skill_triggers": total_skill_triggers,
            "party_details": party_details
        }
    
    def simulate_week(
        self,
        party: List[Pokemon],
        field_bonus: float = 1.57,
        pot_capacity: int = 69,
        recipe_requests: List[str] = None,
        weeks: int = 1
    ) -> Dict[str, Any]:
        """週間シミュレーション"""
        if recipe_requests is None:
            recipe_requests = ["カレー"]
        
        weekly_results = []
        
        for week in range(weeks):
            # 1週間の生産量計算（7日）
            week_production = self.simulate_daily_production(
                party, field_bonus, hours=24.0 * 7
            )
            
            # レシピ作成
            recipe_results = {}
            total_recipe_energy = 0.0
            remaining_ingredients = week_production["total_ingredients"].copy()
            
            for recipe_name in recipe_requests:
                recipe_result = self.recipe_calculator.calculate_recipe_energy(
                    recipe_name,
                    remaining_ingredients,
                    recipe_level=5,  # デフォルトレベル5
                    pot_capacity=pot_capacity
                )
                
                recipe_results[recipe_name] = recipe_result
                total_recipe_energy += recipe_result["energy"]
                
                # 使用した食材を減算
                for ingredient, used in recipe_result["ingredients_used"].items():
                    remaining_ingredients[ingredient] = max(0, 
                        remaining_ingredients.get(ingredient, 0) - used)
            
            weekly_results.append({
                "week": week + 1,
                "berry_energy": week_production["total_berry_energy"],
                "recipe_energy": total_recipe_energy,
                "total_energy": week_production["total_berry_energy"] + total_recipe_energy,
                "ingredients_produced": week_production["total_ingredients"],
                "ingredients_remaining": remaining_ingredients,
                "recipes": recipe_results,
                "skill_triggers": week_production["total_skill_triggers"]
            })
        
        # 平均値計算
        avg_berry_energy = sum(w["berry_energy"] for w in weekly_results) / weeks
        avg_recipe_energy = sum(w["recipe_energy"] for w in weekly_results) / weeks
        avg_total_energy = sum(w["total_energy"] for w in weekly_results) / weeks
        
        return {
            "weeks_simulated": weeks,
            "weekly_results": weekly_results,
            "averages": {
                "berry_energy": avg_berry_energy,
                "recipe_energy": avg_recipe_energy,
                "total_energy": avg_total_energy,
                "daily_energy": avg_total_energy / 7
            },
            "party_composition": [p.name for p in party]
        }


class OptimizationService:
    """最適化サービス"""
    
    def __init__(self):
        """最適化サービスの初期化"""
        self.simulator = PartySimulator()
        self.data_manager = pokemon_data_manager
    
    def find_optimal_party(
        self,
        must_include: List[str] = None,
        field_bonus: float = 1.57,
        pot_capacity: int = 69,
        recipe_requests: List[str] = None,
        weeks_to_simulate: int = 3,
        max_combinations: int = 1000
    ) -> Dict[str, Any]:
        """最適パーティの探索"""
        if must_include is None:
            must_include = []
        if recipe_requests is None:
            recipe_requests = ["カレー"]
        
        # 利用可能なポケモンリスト
        available_pokemon = self.data_manager.get_available_pokemon_names()
        
        # 必須ポケモンの妥当性チェック
        for name in must_include:
            if name not in available_pokemon:
                raise ValueError(f"不明なポケモン名: {name}")
        
        # 残りの枠数計算
        remaining_slots = 5 - len(must_include)
        if remaining_slots < 0:
            raise ValueError("必須ポケモンが5匹を超えています")
        
        # 候補ポケモン（必須以外）
        candidate_pokemon = [name for name in available_pokemon if name not in must_include]
        
        best_party = None
        best_energy = 0.0
        evaluated_combinations = 0
        
        logger.info(f"Starting optimization: {remaining_slots} slots, {len(candidate_pokemon)} candidates")
        
        # 組み合わせの生成と評価
        if remaining_slots == 0:
            # 必須ポケモンのみ
            combinations_to_check = [must_include]
        else:
            combinations_to_check = combinations(candidate_pokemon, remaining_slots)
        
        for combination in combinations_to_check:
            if evaluated_combinations >= max_combinations:
                logger.warning(f"Reached maximum combinations limit: {max_combinations}")
                break
            
            # パーティ構成
            party_names = must_include + list(combination)
            
            try:
                # ポケモンインスタンス作成
                party = [
                    self.data_manager.create_pokemon(name, level=50)
                    for name in party_names
                ]
                
                # シミュレーション実行
                result = self.simulator.simulate_week(
                    party=party,
                    field_bonus=field_bonus,
                    pot_capacity=pot_capacity,
                    recipe_requests=recipe_requests,
                    weeks=weeks_to_simulate
                )
                
                avg_energy = result["averages"]["total_energy"]
                
                if avg_energy > best_energy:
                    best_energy = avg_energy
                    best_party = {
                        "party_names": party_names,
                        "simulation_result": result
                    }
                
                evaluated_combinations += 1
                
            except Exception as e:
                logger.error(f"Error evaluating party {party_names}: {e}")
                continue
        
        if best_party is None:
            raise RuntimeError("最適なパーティを見つけることができませんでした")
        
        logger.info(f"Optimization completed: evaluated {evaluated_combinations} combinations")
        
        return {
            "best_party": best_party["party_names"],
            "best_energy": best_energy,
            "simulation_result": best_party["simulation_result"],
            "optimization_stats": {
                "evaluated_combinations": evaluated_combinations,
                "total_candidates": len(candidate_pokemon),
                "must_include": must_include,
                "remaining_slots": remaining_slots
            }
        }
    
    def evaluate_specific_party(
        self,
        party_names: List[str],
        field_bonus: float = 1.57,
        pot_capacity: int = 69,
        recipe_requests: List[str] = None,
        weeks_to_simulate: int = 3
    ) -> Dict[str, Any]:
        """特定パーティの評価"""
        if recipe_requests is None:
            recipe_requests = ["カレー"]
        
        # パーティの妥当性チェック
        validation = self.data_manager.validate_party_composition(party_names)
        if not validation["valid"]:
            raise ValueError(f"不正なパーティ構成: {validation['errors']}")
        
        try:
            # ポケモンインスタンス作成
            party = [
                self.data_manager.create_pokemon(name, level=50)
                for name in party_names
            ]
            
            # シミュレーション実行
            result = self.simulator.simulate_week(
                party=party,
                field_bonus=field_bonus,
                pot_capacity=pot_capacity,
                recipe_requests=recipe_requests,
                weeks=weeks_to_simulate
            )
            
            return {
                "party_names": party_names,
                "simulation_result": result,
                "validation": validation
            }
            
        except Exception as e:
            logger.error(f"Error evaluating party {party_names}: {e}")
            raise RuntimeError(f"パーティ評価に失敗しました: {e}")


# グローバルインスタンス
optimization_service = OptimizationService()