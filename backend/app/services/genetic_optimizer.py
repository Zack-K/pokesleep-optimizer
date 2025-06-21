"""
遺伝的アルゴリズム最適化サービス
パーティ編成の高度な最適化を実現
"""
import random
import logging
from typing import List, Dict, Any, Tuple, Optional, Callable
import numpy as np
from dataclasses import dataclass, field
from .simulation_service import optimization_service

logger = logging.getLogger(__name__)


@dataclass
class Individual:
    """個体（パーティ）クラス"""
    genes: List[str]  # ポケモン名のリスト
    fitness: Optional[float] = None
    evaluated: bool = False
    
    def __post_init__(self):
        """初期化後の処理: 重複排除と検証"""
        self.genes = self._ensure_unique_genes(self.genes)
    
    def _ensure_unique_genes(self, genes: List[str]) -> List[str]:
        """重複を排除し、一意な遺伝子のリストを保証"""
        if not genes:
            return []
        
        unique_genes = []
        seen = set()
        
        for gene in genes:
            if gene not in seen:
                unique_genes.append(gene)
                seen.add(gene)
        
        return unique_genes
    
    def mutate(self, available_pokemon: List[str], mutation_rate: float = 0.1) -> 'Individual':
        """突然変異を実行（重複なし）"""
        mutated_genes = self.genes.copy()
        
        for i in range(len(mutated_genes)):
            if random.random() < mutation_rate:
                # 重複を避けてランダムなポケモンに置き換え
                current_pokemon = mutated_genes[i]
                other_pokemon = [p for j, p in enumerate(mutated_genes) if j != i]
                available_candidates = [p for p in available_pokemon if p not in other_pokemon]
                
                if available_candidates:
                    mutated_genes[i] = random.choice(available_candidates)
        
        return Individual(mutated_genes)
    
    @staticmethod
    def crossover(parent1: 'Individual', parent2: 'Individual', available_pokemon: List[str]) -> Tuple['Individual', 'Individual']:
        """交叉を実行（単純な均等交叉）"""
        size = len(parent1.genes)
        
        child1_genes = []
        child2_genes = []
        
        # 交叉マスクを生成
        for i in range(size):
            if random.random() < 0.5:
                child1_genes.append(parent1.genes[i])
                child2_genes.append(parent2.genes[i])
            else:
                child1_genes.append(parent2.genes[i])
                child2_genes.append(parent1.genes[i])
        
        # 重複除去と補完
        def fix_duplicates(genes: List[str]) -> List[str]:
            unique_genes = []
            used = set()
            
            for gene in genes:
                if gene not in used:
                    unique_genes.append(gene)
                    used.add(gene)
                else:
                    # 重複の場合、利用可能なポケモンから選択
                    candidates = [p for p in available_pokemon if p not in used]
                    if candidates:
                        replacement = random.choice(candidates)
                        unique_genes.append(replacement)
                        used.add(replacement)
                    else:
                        unique_genes.append(gene)  # 候補がない場合はそのまま
            
            return unique_genes
        
        child1_genes = fix_duplicates(child1_genes)
        child2_genes = fix_duplicates(child2_genes)
        
        return Individual(child1_genes), Individual(child2_genes)


@dataclass
class Population:
    """個体群クラス"""
    individuals: List[Individual] = field(default_factory=list)
    
    @classmethod
    def create_random(cls, population_size: int, party_size: int, 
                     available_pokemon: List[str], must_include: List[str] = None) -> 'Population':
        """ランダムな個体群を生成"""
        if must_include is None:
            must_include = []
        
        individuals = []
        remaining_slots = party_size - len(must_include)
        available_candidates = [p for p in available_pokemon if p not in must_include]
        
        for _ in range(population_size):
            # 確実に重複なしの個体を生成
            genes = cls._generate_unique_party(
                party_size=party_size,
                available_pokemon=available_pokemon,
                must_include=must_include
            )
            individuals.append(Individual(genes))
        
        return cls(individuals)
    
    @classmethod
    def _generate_unique_party(cls, party_size: int, available_pokemon: List[str], 
                              must_include: List[str] = None) -> List[str]:
        """重複なしのパーティを確実に生成"""
        if must_include is None:
            must_include = []
        
        # 必須ポケモンから開始
        party = must_include.copy()
        remaining_slots = party_size - len(party)
        
        # 利用可能な候補（必須ポケモンを除く）
        available_candidates = [p for p in available_pokemon if p not in party]
        
        if remaining_slots > 0:
            if len(available_candidates) >= remaining_slots:
                # 十分な候補がある場合: ランダムサンプリング
                selected = random.sample(available_candidates, remaining_slots)
                party.extend(selected)
            else:
                # 候補不足の場合: 利用可能な全候補を追加
                party.extend(available_candidates)
                
                # まだ不足している場合、必須ポケモン以外から重複選択
                while len(party) < party_size:
                    non_required = [p for p in available_pokemon if p not in must_include]
                    if non_required:
                        party.append(random.choice(non_required))
                    else:
                        # 最後の手段: 利用可能ポケモンから選択
                        party.append(random.choice(available_pokemon))
                
                # 重複除去
                unique_party = []
                seen = set()
                for pokemon in party:
                    if pokemon not in seen:
                        unique_party.append(pokemon)
                        seen.add(pokemon)
                    if len(unique_party) >= party_size:
                        break
                party = unique_party
        
        # パーティサイズに合わせて調整
        if len(party) > party_size:
            party = party[:party_size]
        elif len(party) < party_size:
            # 不足分を補完
            while len(party) < party_size and available_pokemon:
                candidate = random.choice(available_pokemon)
                if candidate not in party:
                    party.append(candidate)
        
        return party
    
    def evaluate(self, fitness_function: 'FitnessFunction'):
        """個体群の適応度を評価"""
        for individual in self.individuals:
            if not individual.evaluated:
                individual.fitness = fitness_function.evaluate(individual.genes)
                individual.evaluated = True
    
    def select_top_k(self, k: int) -> List[Individual]:
        """上位k個体を選択"""
        evaluated_individuals = [ind for ind in self.individuals if ind.evaluated and ind.fitness is not None]
        sorted_individuals = sorted(evaluated_individuals, key=lambda x: x.fitness, reverse=True)
        return sorted_individuals[:k]
    
    def tournament_selection(self, tournament_size: int = 3) -> Individual:
        """トーナメント選択"""
        tournament = random.sample(self.individuals, min(tournament_size, len(self.individuals)))
        return max(tournament, key=lambda x: x.fitness if x.fitness is not None else -float('inf'))


class FitnessFunction:
    """適応度関数クラス"""
    
    def __init__(self, field_bonus: float = 1.57, pot_capacity: int = 69,
                 recipe_requests: List[str] = None, weeks_to_simulate: int = 3):
        """
        適応度関数の初期化
        
        Args:
            field_bonus: フィールドボーナス
            pot_capacity: 鍋容量
            recipe_requests: レシピリクエスト
            weeks_to_simulate: シミュレーション週数
        """
        self.field_bonus = field_bonus
        self.pot_capacity = pot_capacity
        self.recipe_requests = recipe_requests or ["カレー"]
        self.weeks_to_simulate = weeks_to_simulate
    
    def evaluate(self, genes: List[str]) -> float:
        """パーティの適応度を評価"""
        try:
            result = optimization_service.evaluate_specific_party(
                party_names=genes,
                field_bonus=self.field_bonus,
                pot_capacity=self.pot_capacity,
                recipe_requests=self.recipe_requests,
                weeks_to_simulate=self.weeks_to_simulate
            )
            
            # 総エナジーを適応度として使用
            total_energy = result["simulation_result"]["averages"]["total_energy"]
            return total_energy
            
        except Exception as e:
            logger.error(f"適応度評価エラー: {e}")
            return 0.0


class GeneticOptimizer:
    """遺伝的アルゴリズム最適化クラス"""
    
    def __init__(self, available_pokemon: List[str], population_size: int = 50,
                 elite_size: int = 10, mutation_rate: float = 0.1, 
                 crossover_rate: float = 0.8, max_generations: int = 100,
                 convergence_threshold: float = 0.01, convergence_generations: int = 5):
        """
        遺伝的アルゴリズム最適化器の初期化
        
        Args:
            available_pokemon: 利用可能なポケモンリスト
            population_size: 個体群サイズ
            elite_size: エリート個体数
            mutation_rate: 突然変異率
            crossover_rate: 交叉率
            max_generations: 最大世代数
            convergence_threshold: 収束判定閾値
            convergence_generations: 収束判定世代数
        """
        self.available_pokemon = available_pokemon
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations
        self.convergence_threshold = convergence_threshold
        self.convergence_generations = convergence_generations
    
    def optimize(self, must_include: List[str] = None, field_bonus: float = 1.57,
                pot_capacity: int = 69, recipe_requests: List[str] = None,
                weeks_to_simulate: int = 3) -> Dict[str, Any]:
        """
        遺伝的アルゴリズムによる最適化実行
        
        Args:
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
        
        logger.info(f"遺伝的アルゴリズム最適化開始: 個体群{self.population_size}, 世代{self.max_generations}")
        
        # 適応度関数の初期化
        fitness_function = FitnessFunction(
            field_bonus=field_bonus,
            pot_capacity=pot_capacity,
            recipe_requests=recipe_requests,
            weeks_to_simulate=weeks_to_simulate
        )
        
        # 初期個体群の生成
        population = self._create_initial_population(must_include)
        
        # 進化履歴の記録
        convergence_history = []
        best_fitness_history = []
        
        for generation in range(self.max_generations):
            # 適応度評価
            population.evaluate(fitness_function)
            
            # 統計情報の記録
            fitness_values = [ind.fitness for ind in population.individuals if ind.fitness is not None]
            if fitness_values:
                best_fitness = max(fitness_values)
                avg_fitness = sum(fitness_values) / len(fitness_values)
                
                convergence_history.append({
                    "generation": generation,
                    "best_fitness": best_fitness,
                    "average_fitness": avg_fitness,
                    "fitness_std": np.std(fitness_values)
                })
                best_fitness_history.append(best_fitness)
                
                logger.info(f"世代 {generation}: 最良適応度 {best_fitness:.2f}, 平均適応度 {avg_fitness:.2f}")
            
            # 収束判定
            if self._check_convergence(best_fitness_history):
                logger.info(f"収束判定により最適化終了: 世代 {generation}")
                break
            
            # 次世代の生成
            population = self._create_next_generation(population, must_include)
        
        # 最終結果の取得
        population.evaluate(fitness_function)
        best_individual = population.select_top_k(1)[0]
        
        return {
            "best_individual": best_individual.genes,
            "best_fitness": best_individual.fitness,
            "generations_completed": generation + 1,
            "convergence_history": convergence_history,
            "final_population_stats": {
                "size": len(population.individuals),
                "evaluated": sum(1 for ind in population.individuals if ind.evaluated)
            }
        }
    
    def _create_initial_population(self, must_include: List[str]) -> Population:
        """初期個体群を作成"""
        return Population.create_random(
            population_size=self.population_size,
            party_size=5,
            available_pokemon=self.available_pokemon,
            must_include=must_include
        )
    
    def _create_next_generation(self, current_population: Population, 
                              must_include: List[str]) -> Population:
        """次世代の個体群を生成"""
        new_individuals = []
        
        # エリート個体の保存
        elite_individuals = current_population.select_top_k(self.elite_size)
        new_individuals.extend(elite_individuals)
        
        # 残りを交叉と突然変異で生成
        while len(new_individuals) < self.population_size:
            if random.random() < self.crossover_rate:
                # 交叉による生成
                parent1 = current_population.tournament_selection()
                parent2 = current_population.tournament_selection()
                child1, child2 = Individual.crossover(parent1, parent2, self.available_pokemon)
                
                # 必須ポケモンの制約を適用
                child1 = self._apply_constraints(child1, must_include)
                child2 = self._apply_constraints(child2, must_include)
                
                new_individuals.extend([child1, child2])
            else:
                # 突然変異による生成
                parent = current_population.tournament_selection()
                child = parent.mutate(self.available_pokemon, self.mutation_rate)
                child = self._apply_constraints(child, must_include)
                new_individuals.append(child)
        
        # 個体群サイズに調整
        new_individuals = new_individuals[:self.population_size]
        
        return Population(new_individuals)
    
    def _apply_constraints(self, individual: Individual, must_include: List[str]) -> Individual:
        """個体に制約を適用"""
        if not must_include:
            return individual
        
        genes = individual.genes.copy()
        
        # 必須ポケモンが含まれているかチェック
        for required_pokemon in must_include:
            if required_pokemon not in genes:
                # ランダムな位置を必須ポケモンに置き換え
                replace_index = random.randint(0, len(genes) - 1)
                genes[replace_index] = required_pokemon
        
        return Individual(genes)
    
    def _check_convergence(self, fitness_history: List[float]) -> bool:
        """収束判定"""
        if len(fitness_history) < self.convergence_generations:
            return False
        
        # 過去n世代の適応度変化を確認
        recent_fitness = fitness_history[-self.convergence_generations:]
        fitness_change = abs(max(recent_fitness) - min(recent_fitness))
        
        return fitness_change < self.convergence_threshold