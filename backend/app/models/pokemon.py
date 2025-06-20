"""
Pokemon ドメインモデル
FastAPI ベストプラクティスに従ったドメインモデル実装
"""
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from ..core.constants import (
    POKEMON_BASE_DATA, PROBABILITY, INVENTORY, BERRY, FOOD,
    MS_CHARGE_STRENGTH_S, MS_DREAM_SHARD_MAGNET_S, MS_ENERGIZING_CHEER_S,
    MS_ENERGY_CHARGE_S, MS_ENERGY_4_EVERYONE, MS_EXTRA_HELPFUL_S,
    MS_INGREDIENT_MAGNET_S, MS_COOKING_POWER_UP_S, MS_METRONOME,
    MS_TASTY_CHANCE, MS_HELPER_BOOST
)


@dataclass
class PokemonNature:
    """ポケモンの性格データクラス"""
    freq: int = 0  # おてつだいスピード補正 (-2 to 2)
    vitality: int = 0  # げんき補正 (-1 to 1) 
    exp: int = 0  # けいけんち補正 (-1 to 1)
    ingr: int = 0  # 食材確率補正 (-1 to 1)
    skill: int = 0  # スキル確率補正 (-1 to 1)


@dataclass  
class PokemonSubSkill:
    """ポケモンのサブスキルデータクラス"""
    skill: int = 0  # スキル確率アップ
    speed: int = 0  # おてつだいスピードアップ
    ingr: int = 0  # 食材確率アップ
    exp: int = 0  # けいけんちボーナス
    help_bonus: int = 0  # おてつだいボーナス
    berry: int = 0  # きのみの数S
    inventory: int = 0  # 最大所持数アップ
    skill_lv_up: int = 0  # スキルレベルアップ


class Pokemon:
    """Pokemonドメインモデル"""
    
    def __init__(
        self,
        name: str,
        level: int = 1,
        nature: Optional[PokemonNature] = None,
        sub_skill: Optional[PokemonSubSkill] = None,
        ribbon: int = 0
    ):
        """
        ポケモンインスタンスの初期化
        
        Args:
            name: ポケモン名
            level: レベル (1-100)
            nature: 性格補正
            sub_skill: サブスキル
            ribbon: リボン数
        """
        if name not in POKEMON_BASE_DATA:
            raise ValueError(f"不明なポケモン名: {name}")
            
        self.name = name
        self.level = max(1, min(100, level))
        self.nature = nature or PokemonNature()
        self.sub_skill = sub_skill or PokemonSubSkill()
        self.ribbon = max(0, ribbon)
        
        # 基本データの読み込み
        base_data = POKEMON_BASE_DATA[name]
        self.kind = base_data["kind"]
        self.type = base_data["type"]
        self.base_freq = base_data["freq"]
        self.berry = base_data["berry"]
        self.ingredients = base_data["ingr"]
        self.main_skill = base_data["main_skill"]
        
        # 確率データの読み込み
        prob_data = PROBABILITY.get(name, {"skill": 0.0, "ingr": 0.0})
        self.base_skill_prob = prob_data["skill"] / 100.0
        self.base_ingr_prob = prob_data["ingr"] / 100.0
        
        # インベントリサイズ
        self.base_inventory = INVENTORY.get(name, 10)
    
    @property
    def effective_frequency(self) -> float:
        """実効おてつだい頻度の計算"""
        # 性格補正
        nature_bonus = 1.0
        if self.nature.freq == 2:
            nature_bonus = 0.8
        elif self.nature.freq == 1:
            nature_bonus = 0.9
        elif self.nature.freq == -1:
            nature_bonus = 1.1
        elif self.nature.freq == -2:
            nature_bonus = 1.2
            
        # サブスキル補正
        speed_bonus = 1.0 - (self.sub_skill.speed * 0.05)
        
        return self.base_freq * nature_bonus * speed_bonus
    
    @property
    def skill_probability(self) -> float:
        """実効スキル発動確率の計算"""
        # 性格補正
        nature_bonus = 1.0 + (self.nature.skill * 0.2)
        
        # サブスキル補正  
        subskill_bonus = 1.0 + (self.sub_skill.skill * 0.1)
        
        return min(1.0, self.base_skill_prob * nature_bonus * subskill_bonus)
    
    @property
    def ingredient_probability(self) -> float:
        """実効食材確率の計算"""
        # 性格補正
        nature_bonus = 1.0 + (self.nature.ingr * 0.2)
        
        # サブスキル補正
        subskill_bonus = 1.0 + (self.sub_skill.ingr * 0.1)
        
        return min(1.0, self.base_ingr_prob * nature_bonus * subskill_bonus)
    
    @property
    def inventory_size(self) -> int:
        """実効インベントリサイズの計算"""
        return self.base_inventory + self.sub_skill.inventory
    
    @property 
    def berry_energy(self) -> int:
        """きのみエナジーの取得"""
        return BERRY.get(self.berry, 0)
    
    def get_ingredient_energy(self, ingredient: str) -> int:
        """指定食材のエナジー値を取得"""
        return FOOD.get(ingredient, 0)
    
    def get_total_ingredient_energy(self) -> int:
        """全食材の合計エナジー値を取得"""
        return sum(self.get_ingredient_energy(ingr) for ingr in self.ingredients)
    
    def calculate_help_amount(self, hours: float = 24.0) -> Dict[str, float]:
        """指定時間内のおてつだい回数を計算"""
        help_per_hour = 3600.0 / self.effective_frequency
        total_helps = help_per_hour * hours
        
        skill_helps = total_helps * self.skill_probability
        ingredient_helps = total_helps * self.ingredient_probability  
        berry_helps = total_helps - skill_helps - ingredient_helps
        
        return {
            "total": total_helps,
            "berry": berry_helps,
            "ingredient": ingredient_helps,
            "skill": skill_helps
        }
    
    def calculate_daily_energy(self, field_bonus: float = 1.0) -> float:
        """1日の獲得エナジーを計算"""
        helps = self.calculate_help_amount(24.0)
        
        # きのみエナジー
        berry_energy = helps["berry"] * self.berry_energy * field_bonus
        
        # 食材エナジー（平均値）
        avg_ingredient_energy = self.get_total_ingredient_energy() / len(self.ingredients)
        ingredient_energy = helps["ingredient"] * avg_ingredient_energy
        
        return berry_energy + ingredient_energy
    
    def get_skill_effect(self, party_size: int = 5) -> Dict[str, Any]:
        """メインスキルの効果を取得"""
        skill_effects = {
            MS_CHARGE_STRENGTH_S: {"type": "strength", "value": 400},
            MS_DREAM_SHARD_MAGNET_S: {"type": "dream_shard", "value": 240},
            MS_ENERGIZING_CHEER_S: {"type": "energizing", "value": 14},
            MS_ENERGY_CHARGE_S: {"type": "energy_charge", "value": 12},
            MS_ENERGY_4_EVERYONE: {"type": "energy_everyone", "value": 5 * party_size},
            MS_EXTRA_HELPFUL_S: {"type": "extra_help", "value": 5},
            MS_INGREDIENT_MAGNET_S: {"type": "ingredient_magnet", "value": 6},
            MS_COOKING_POWER_UP_S: {"type": "cooking_power", "value": 7},
            MS_METRONOME: {"type": "metronome", "value": "random"},
            MS_TASTY_CHANCE: {"type": "tasty_chance", "value": 7},
            MS_HELPER_BOOST: {"type": "helper_boost", "value": 5}
        }
        
        return skill_effects.get(self.main_skill, {"type": "unknown", "value": 0})
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式でのデータ出力"""
        return {
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "kind": self.kind,
            "berry": self.berry,
            "berry_energy": self.berry_energy,
            "ingredients": self.ingredients,
            "main_skill": self.main_skill,
            "frequency": self.effective_frequency,
            "skill_probability": self.skill_probability,
            "ingredient_probability": self.ingredient_probability,
            "inventory_size": self.inventory_size,
            "nature": {
                "freq": self.nature.freq,
                "vitality": self.nature.vitality,
                "exp": self.nature.exp,
                "ingr": self.nature.ingr,
                "skill": self.nature.skill
            },
            "sub_skill": {
                "skill": self.sub_skill.skill,
                "speed": self.sub_skill.speed,
                "ingr": self.sub_skill.ingr,
                "exp": self.sub_skill.exp,
                "help_bonus": self.sub_skill.help_bonus,
                "berry": self.sub_skill.berry,
                "inventory": self.sub_skill.inventory,
                "skill_lv_up": self.sub_skill.skill_lv_up
            }
        }
    
    def __str__(self) -> str:
        return f"Pokemon({self.name}, Lv.{self.level}, {self.type})"
    
    def __repr__(self) -> str:
        return self.__str__()