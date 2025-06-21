"""
マルチ目的最適化サービス
エナジー効率、レシピバランス、食材多様性の同時最適化
"""
import logging
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .simulation_service import optimization_service
from .genetic_optimizer import GeneticOptimizer, Individual, Population

logger = logging.getLogger(__name__)


@dataclass
class Solution:
    """最適化解クラス"""
    party: List[str]
    objectives: List[float]
    fitness: Optional[float] = None


class ObjectiveFunction:
    """目的関数クラス"""
    
    def __init__(self, name: str, maximize: bool = True, weight: float = 1.0):
        """
        目的関数の初期化
        
        Args:
            name: 目的関数名
            maximize: 最大化するかどうか
            weight: 重み
        """
        self.name = name
        self.maximize = maximize
        self.weight = weight
    
    def evaluate(self, party_data: Dict[str, Any]) -> float:
        """目的関数を評価（サブクラスで実装）"""
        raise NotImplementedError
    
    @classmethod
    def create_energy_efficiency(cls) -> 'ObjectiveFunction':
        """エナジー効率目的関数を作成"""
        obj = cls("energy_efficiency", maximize=True)
        obj.evaluate = lambda data: data["simulation_result"]["averages"]["total_energy"]
        return obj
    
    @classmethod
    def create_recipe_balance(cls) -> 'ObjectiveFunction':
        """レシピバランス目的関数を作成"""
        obj = cls("recipe_balance", maximize=False)  # 分散を最小化
        
        def evaluate_balance(data):
            try:
                weekly_results = data["simulation_result"]["weekly_results"]
                if not weekly_results:
                    return float('inf')
                
                # 各レシピの作成数を取得
                recipe_counts = []
                for recipe_name, recipe_data in weekly_results[0]["recipes"].items():
                    recipe_counts.append(recipe_data.get("count", 0))
                
                if not recipe_counts:
                    return float('inf')
                
                # 分散を計算（バランスが良いほど分散が小さい）
                return np.var(recipe_counts)
                
            except Exception as e:
                logger.error(f"レシピバランス評価エラー: {e}")
                return float('inf')
        
        obj.evaluate = evaluate_balance
        return obj
    
    @classmethod
    def create_ingredient_diversity(cls) -> 'ObjectiveFunction':
        """食材多様性目的関数を作成"""
        obj = cls("ingredient_diversity", maximize=True)
        
        def evaluate_diversity(data):
            try:
                weekly_results = data["simulation_result"]["weekly_results"]
                if not weekly_results:
                    return 0.0
                
                # 食材の種類数と量のバランスを評価
                ingredients = weekly_results[0].get("ingredients_produced", {})
                if not ingredients:
                    return 0.0
                
                # シャノンの多様性指数を計算
                total_count = sum(ingredients.values())
                if total_count == 0:
                    return 0.0
                
                diversity_index = 0.0
                for count in ingredients.values():
                    if count > 0:
                        p = count / total_count
                        diversity_index -= p * np.log(p)
                
                return diversity_index
                
            except Exception as e:
                logger.error(f"食材多様性評価エラー: {e}")
                return 0.0
        
        obj.evaluate = evaluate_diversity
        return obj


class ParetoFront:
    """パレート最適解フロントクラス"""
    
    def __init__(self):
        """パレート最適解フロントの初期化"""
        self.solutions: List[Solution] = []
    
    def add_solution(self, party: List[str], objectives: List[float]):
        """解をフロントに追加"""
        new_solution = Solution(party, objectives)
        
        # 既存の解との支配関係をチェック
        non_dominated = []
        is_dominated = False
        
        for existing_solution in self.solutions:
            if self._dominates(objectives, existing_solution.objectives):
                # 新しい解が既存の解を支配する場合、既存の解は除外
                continue
            elif self._dominates(existing_solution.objectives, objectives):
                # 既存の解が新しい解を支配する場合、新しい解は追加しない
                is_dominated = True
                non_dominated.append(existing_solution)
            else:
                # 非支配関係
                non_dominated.append(existing_solution)
        
        if not is_dominated:
            non_dominated.append(new_solution)
        
        self.solutions = non_dominated
    
    def get_pareto_optimal(self) -> List[Solution]:
        """パレート最適解を取得"""
        return self.solutions.copy()
    
    def _dominates(self, objectives1: List[float], objectives2: List[float]) -> bool:
        """支配関係を判定"""
        if len(objectives1) != len(objectives2):
            return False
        
        # 全ての目的で objectives1 >= objectives2 かつ少なくとも1つで objectives1 > objectives2
        better_or_equal = all(o1 >= o2 for o1, o2 in zip(objectives1, objectives2))
        strictly_better = any(o1 > o2 for o1, o2 in zip(objectives1, objectives2))
        
        return better_or_equal and strictly_better


class ScalarizationMethod:
    """スカラー化手法クラス"""
    
    def __init__(self, method_type: str, weights: List[float], 
                 maximize: List[bool], **kwargs):
        """
        スカラー化手法の初期化
        
        Args:
            method_type: スカラー化手法の種類
            weights: 各目的関数の重み
            maximize: 各目的関数が最大化かどうか
            **kwargs: 追加パラメータ
        """
        self.method_type = method_type
        self.weights = weights
        self.maximize = maximize
        self.kwargs = kwargs
    
    def scalarize(self, objectives: List[float]) -> float:
        """目的関数値をスカラー値に変換"""
        if self.method_type == "weighted_sum":
            return self._weighted_sum(objectives)
        elif self.method_type == "chebyshev":
            return self._chebyshev(objectives)
        else:
            raise ValueError(f"未知のスカラー化手法: {self.method_type}")
    
    def _weighted_sum(self, objectives: List[float]) -> float:
        """重み付き和スカラー化"""
        score = 0.0
        for obj, weight, is_max in zip(objectives, self.weights, self.maximize):
            if is_max:
                score += weight * obj
            else:
                score += weight * (1.0 - obj)  # 最小化目的は反転
        return score
    
    def _chebyshev(self, objectives: List[float]) -> float:
        """チェビシェフ法スカラー化"""
        reference_point = self.kwargs.get("reference_point", [1.0] * len(objectives))
        
        max_deviation = 0.0
        for obj, ref, weight, is_max in zip(objectives, reference_point, 
                                          self.weights, self.maximize):
            if is_max:
                deviation = weight * abs(ref - obj)
            else:
                deviation = weight * abs(obj - ref)
            max_deviation = max(max_deviation, deviation)
        
        return -max_deviation  # 最小化するため負の値を返す
    
    @classmethod
    def create_weighted_sum(cls, weights: List[float], maximize: List[bool]) -> 'ScalarizationMethod':
        """重み付き和スカラー化手法を作成"""
        return cls("weighted_sum", weights, maximize)
    
    @classmethod
    def create_chebyshev(cls, reference_point: List[float], 
                        weights: List[float]) -> 'ScalarizationMethod':
        """チェビシェフ法スカラー化手法を作成"""
        maximize = [True] * len(weights)  # 参照点に近づけるため最大化
        return cls("chebyshev", weights, maximize, reference_point=reference_point)


class MultiObjectiveOptimizer:
    """マルチ目的最適化クラス"""
    
    def __init__(self, objectives: List[ObjectiveFunction], 
                 population_size: int = 50, max_generations: int = 100,
                 scalarization_method: Optional[ScalarizationMethod] = None):
        """
        マルチ目的最適化器の初期化
        
        Args:
            objectives: 目的関数リスト
            population_size: 個体群サイズ
            max_generations: 最大世代数
            scalarization_method: スカラー化手法
        """
        self.objectives = objectives
        self.population_size = population_size
        self.max_generations = max_generations
        if scalarization_method is None and len(objectives) > 0:
            self.scalarization_method = ScalarizationMethod.create_weighted_sum(
                [1.0 / len(objectives)] * len(objectives),
                [obj.maximize for obj in objectives]
            )
        else:
            self.scalarization_method = scalarization_method
    
    def optimize(self, available_pokemon: List[str], must_include: List[str] = None,
                field_bonus: float = 1.57, pot_capacity: int = 69,
                recipe_requests: List[str] = None, weeks_to_simulate: int = 3) -> Dict[str, Any]:
        """
        マルチ目的最適化実行
        
        Args:
            available_pokemon: 利用可能なポケモンリスト
            must_include: 必須ポケモンリスト
            field_bonus: フィールドボーナス
            pot_capacity: 鍋容量
            recipe_requests: レシピリクエスト
            weeks_to_simulate: シミュレーション週数
            
        Returns:
            最適化結果辞書
        """
        if must_include is None:
            must_include = []
        if recipe_requests is None:
            recipe_requests = ["カレー"]
        
        logger.info(f"マルチ目的最適化開始: {len(self.objectives)}目的, 個体群{self.population_size}")
        
        # パレート最適解フロント
        pareto_front = ParetoFront()
        
        # 遺伝的アルゴリズムベースの最適化
        genetic_optimizer = GeneticOptimizer(
            available_pokemon=available_pokemon,
            population_size=self.population_size,
            max_generations=self.max_generations
        )
        
        # 複数回実行して解の多様性を確保
        all_objective_values = []
        all_parties = []
        
        for run in range(3):  # 3回実行
            # 重みを変更して異なる解を探索
            weights = self._generate_diverse_weights(run, len(self.objectives))
            self.scalarization_method.weights = weights
            
            # カスタム適応度関数でスカラー化最適化
            def multi_objective_fitness(genes: List[str]) -> float:
                return self._evaluate_multi_objective(
                    genes, field_bonus, pot_capacity, recipe_requests, weeks_to_simulate
                )
            
            # 遺伝的アルゴリズムの適応度関数を置き換え
            genetic_optimizer._fitness_function = multi_objective_fitness
            
            # 単一最適化実行
            result = genetic_optimizer.optimize(
                must_include=must_include,
                field_bonus=field_bonus,
                pot_capacity=pot_capacity,
                recipe_requests=recipe_requests,
                weeks_to_simulate=weeks_to_simulate
            )
            
            # 結果をパレート最適解フロントに追加
            best_party = result["best_individual"]
            objectives = self._evaluate_objectives(
                best_party, field_bonus, pot_capacity, recipe_requests, weeks_to_simulate
            )
            
            pareto_front.add_solution(best_party, objectives)
            all_objective_values.append(objectives)
            all_parties.append(best_party)
        
        # パレート最適解の取得
        pareto_solutions = pareto_front.get_pareto_optimal()
        
        # 最良妥協解の選択（スカラー化値が最大の解）
        best_compromise = None
        best_scalarized_value = -float('inf')
        
        for solution in pareto_solutions:
            normalized_objectives = self._normalize_objectives([solution.objectives])[0]
            scalarized_value = self.scalarization_method.scalarize(normalized_objectives)
            
            if scalarized_value > best_scalarized_value:
                best_scalarized_value = scalarized_value
                best_compromise = solution
        
        return {
            "pareto_front": [(sol.party, sol.objectives) for sol in pareto_solutions],
            "best_compromise": {
                "party": best_compromise.party if best_compromise else [],
                "objectives": best_compromise.objectives if best_compromise else [],
                "scalarized_value": best_scalarized_value
            },
            "objective_values": all_objective_values,
            "generations_completed": self.max_generations,
            "objective_names": [obj.name for obj in self.objectives]
        }
    
    def _evaluate_multi_objective(self, genes: List[str], field_bonus: float,
                                pot_capacity: int, recipe_requests: List[str],
                                weeks_to_simulate: int) -> float:
        """マルチ目的適応度評価"""
        objectives = self._evaluate_objectives(
            genes, field_bonus, pot_capacity, recipe_requests, weeks_to_simulate
        )
        
        # 正規化してスカラー化
        normalized_objectives = self._normalize_objectives([objectives])[0]
        return self.scalarization_method.scalarize(normalized_objectives)
    
    def _evaluate_objectives(self, genes: List[str], field_bonus: float,
                           pot_capacity: int, recipe_requests: List[str],
                           weeks_to_simulate: int) -> List[float]:
        """全目的関数の評価"""
        try:
            # シミュレーション実行
            party_data = optimization_service.evaluate_specific_party(
                party_names=genes,
                field_bonus=field_bonus,
                pot_capacity=pot_capacity,
                recipe_requests=recipe_requests,
                weeks_to_simulate=weeks_to_simulate
            )
            
            # 各目的関数を評価
            objectives = []
            for obj_func in self.objectives:
                obj_value = obj_func.evaluate(party_data)
                objectives.append(obj_value)
            
            return objectives
            
        except Exception as e:
            logger.error(f"目的関数評価エラー: {e}")
            return [0.0] * len(self.objectives)
    
    def _normalize_objectives(self, objectives_data: List[List[float]]) -> List[List[float]]:
        """目的関数値を正規化"""
        if not objectives_data:
            return []
        
        objectives_array = np.array(objectives_data)
        normalized = np.zeros_like(objectives_array)
        
        for i in range(objectives_array.shape[1]):
            col = objectives_array[:, i]
            col_min, col_max = col.min(), col.max()
            
            if col_max > col_min:
                normalized[:, i] = (col - col_min) / (col_max - col_min)
            else:
                normalized[:, i] = 0.5  # 全て同じ値の場合は中央値
        
        return normalized.tolist()
    
    def _generate_diverse_weights(self, run_index: int, num_objectives: int) -> List[float]:
        """多様な重みベクトルを生成"""
        if run_index == 0:
            # 均等重み
            return [1.0 / num_objectives] * num_objectives
        elif run_index == 1:
            # エナジー重視
            weights = [0.1] * num_objectives
            weights[0] = 0.7  # エナジー効率を重視
            return weights
        else:
            # バランス重視
            weights = [0.1] * num_objectives
            if len(weights) > 1:
                weights[1] = 0.7  # レシピバランスを重視
            return weights


class OptimizationObjectives:
    """最適化目的の組み合わせクラス"""
    
    @staticmethod
    def create_balanced() -> List[ObjectiveFunction]:
        """バランス重視の目的関数組み合わせ"""
        return [
            ObjectiveFunction.create_energy_efficiency(),
            ObjectiveFunction.create_recipe_balance()
        ]
    
    @staticmethod
    def create_energy_focused() -> List[ObjectiveFunction]:
        """エナジー重視の目的関数組み合わせ"""
        return [
            ObjectiveFunction.create_energy_efficiency()
        ]
    
    @staticmethod
    def create_recipe_focused() -> List[ObjectiveFunction]:
        """レシピ重視の目的関数組み合わせ"""
        return [
            ObjectiveFunction.create_recipe_balance(),
            ObjectiveFunction.create_ingredient_diversity()
        ]
    
    @staticmethod
    def create_comprehensive() -> List[ObjectiveFunction]:
        """包括的な目的関数組み合わせ"""
        return [
            ObjectiveFunction.create_energy_efficiency(),
            ObjectiveFunction.create_recipe_balance(),
            ObjectiveFunction.create_ingredient_diversity()
        ]