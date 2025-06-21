"""
Pokemon データアクセス層
ポケモンデータの読み込みと管理を担当
"""
from typing import Dict, List, Optional, Any
import logging
from ..models.pokemon import Pokemon, PokemonNature, PokemonSubSkill
from ..core.constants import POKEMON_BASE_DATA, PROBABILITY, INVENTORY
from .pokes_converter import load_pokes_data

logger = logging.getLogger(__name__)


class PokemonDataManager:
    """ポケモンデータの管理クラス"""
    
    def __init__(self):
        """データマネージャーの初期化"""
        self._pokemon_cache: Dict[str, Pokemon] = {}
        self._available_pokemon: List[str] = []
        self._pokemon_data: Dict[str, Dict[str, Any]] = {}
        self._load_status = False
        
        # 初期化時にデータを読み込み
        self._load_all_pokemon_data()
    
    def _load_all_pokemon_data(self):
        """全ポケモンデータの読み込み"""
        try:
            # pokes.pyからの実データを優先的に読み込み
            pokes_data = load_pokes_data()
            
            if pokes_data:
                logger.info(f"Loaded {len(pokes_data)} pokemon from pokes.py")
                self._pokemon_data = pokes_data
                self._available_pokemon = list(pokes_data.keys())
                self._load_status = True
            else:
                # フォールバック: constants.pyのテストデータ
                logger.warning("Failed to load pokes.py, using test data from constants.py")
                self._pokemon_data = self._convert_constants_data()
                self._available_pokemon = list(POKEMON_BASE_DATA.keys())
                self._load_status = True
                
        except Exception as e:
            logger.error(f"Failed to load pokemon data: {e}")
            # 最後の手段: constants.pyのテストデータ
            self._pokemon_data = self._convert_constants_data()
            self._available_pokemon = list(POKEMON_BASE_DATA.keys())
            self._load_status = False
    
    def _convert_constants_data(self) -> Dict[str, Dict[str, Any]]:
        """constants.pyのデータを統一形式に変換"""
        converted = {}
        for name, base_data in POKEMON_BASE_DATA.items():
            prob_data = PROBABILITY.get(name, {"skill": 0.0, "ingr": 0.0})
            inventory_size = INVENTORY.get(name, 10)
            
            converted[name] = {
                "display_name": name,
                "species": name,  # 種族名として使用
                "level": 50,  # デフォルトレベル
                "kind": base_data["kind"],
                "type": base_data["type"],
                "frequency": base_data["freq"],
                "berry": base_data["berry"],
                "berry_energy": 0,  # 後で計算
                "ingredients": base_data["ingr"],
                "main_skill": base_data["main_skill"],
                "skill_probability": prob_data["skill"],
                "ingredient_probability": prob_data["ingr"],
                "inventory_size": inventory_size,
                "nature": {"freq": 0, "vitality": 0, "exp": 0, "ingr": 0, "skill": 0},
                "subskill": {"skill": 0, "speed": 0, "ingr": 0, "exp": 0, "help_bonus": 0, "berry": 0, "inventory": 0, "skill_lv_up": 0, "eng_bonus": 0},
                "main_skill_level": 1,
                "evolution_stage": 0,
                "vitality": 100,
                "ribbon": "AAA",
            }
        return converted
    
    def get_available_pokemon_names(self) -> List[str]:
        """利用可能なポケモン名のリストを取得"""
        return self._available_pokemon.copy()
    
    def get_optimizable_pokemon_names(self) -> List[str]:
        """最適化可能なポケモン名一覧を取得（基本データが存在するもののみ）"""
        from ..core.constants import POKEMON_BASE_DATA
        
        # 基本データが存在するポケモンを優先
        optimizable = []
        
        for name in self._available_pokemon:
            if name in POKEMON_BASE_DATA:
                # 基本データ存在: そのまま追加
                optimizable.append(name)
            elif self._can_generate_base_data(name):
                # 基本データ生成可能: 追加
                optimizable.append(name)
        
        # 最低限のポケモンが確保できない場合はフォールバック
        if len(optimizable) < 10:
            logger.warning(f"最適化可能ポケモンが少なすぎます ({len(optimizable)}体). フォールバック実行")
            return self._get_fallback_pokemon_names()
        
        logger.info(f"最適化可能ポケモン: {len(optimizable)}体")
        return optimizable
    
    def _can_generate_base_data(self, name: str) -> bool:
        """基本データが生成可能かチェック"""
        if name not in self._pokemon_data:
            return False
        
        pokemon_data = self._pokemon_data[name]
        required_fields = ['kind', 'type', 'frequency', 'berry', 'ingredients', 'main_skill']
        
        return all(field in pokemon_data and pokemon_data[field] is not None 
                  for field in required_fields)
    
    def _get_fallback_pokemon_names(self) -> List[str]:
        """フォールバック用の基本ポケモン名リスト"""
        from ..core.constants import POKEMON_BASE_DATA
        
        # 基本データが存在するポケモンを最優先
        base_pokemon = list(POKEMON_BASE_DATA.keys())
        
        if len(base_pokemon) >= 10:
            return base_pokemon[:20]  # 最大20体に制限
        
        # 基本データが不足している場合、生成可能なものを追加
        additional = []
        for name in self._available_pokemon:
            if name not in base_pokemon and self._can_generate_base_data(name):
                additional.append(name)
                if len(base_pokemon) + len(additional) >= 15:
                    break
        
        return base_pokemon + additional
    
    def get_pokemon_count(self) -> int:
        """利用可能なポケモンの数を取得"""
        return len(self._available_pokemon)
    
    def is_valid_pokemon_name(self, name: str) -> bool:
        """ポケモン名の有効性をチェック"""
        return name in self._pokemon_data
    
    def get_or_generate_base_data(self, name: str) -> Dict[str, Any]:
        """基本データを取得、なければ動的生成"""
        from ..core.constants import POKEMON_BASE_DATA
        
        # 既存の基本データをチェック
        if name in POKEMON_BASE_DATA:
            return POKEMON_BASE_DATA[name]
        
        # 実データから基本データを生成
        if name in self._pokemon_data:
            pokemon_data = self._pokemon_data[name]
            return self._generate_base_data_from_real_data(pokemon_data)
        
        # 最終フォールバック: デフォルト基本データ
        logger.warning(f"ポケモン '{name}' の基本データを生成できません。デフォルト値を使用。")
        return self._get_default_base_data()
    
    def _generate_base_data_from_real_data(self, pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
        """実データから基本データを生成"""
        return {
            "kind": pokemon_data.get("kind", 1),
            "type": pokemon_data.get("type", "きのみ"),
            "freq": pokemon_data.get("frequency", 3000),
            "berry": pokemon_data.get("berry", "オレンのみ"),
            "ingr": pokemon_data.get("ingredients", ["エッグ", "ミルク", "リンゴ"]),
            "main_skill": pokemon_data.get("main_skill", 1),
            # 確率データも含める
            "skill_probability": pokemon_data.get("skill_probability", 0.0),
            "ingredient_probability": pokemon_data.get("ingredient_probability", 0.0),
        }
    
    def _get_default_base_data(self) -> Dict[str, Any]:
        """デフォルト基本データ"""
        return {
            "kind": 1,  # ノーマル
            "type": "きのみ",
            "freq": 3000,
            "berry": "オレンのみ",
            "ingr": ["エッグ", "ミルク", "リンゴ"],
            "main_skill": 1,
        }

    def create_pokemon(
        self,
        name: str,
        level: int = 50,
        nature: Optional[Dict[str, int]] = None,
        sub_skill: Optional[Dict[str, int]] = None,
        ribbon: int = 0
    ) -> Pokemon:
        """
        ポケモンインスタンスを作成
        
        Args:
            name: ポケモン名
            level: レベル
            nature: 性格補正
            sub_skill: サブスキル
            ribbon: リボン数
            
        Returns:
            Pokemon: ポケモンインスタンス
            
        Raises:
            ValueError: 不正なポケモン名の場合
        """
        # 基本データの取得または生成を試行
        try:
            base_data = self.get_or_generate_base_data(name)
        except Exception as e:
            raise ValueError(f"ポケモン '{name}' のデータを取得できません: {e}")
        
        # 性格データの変換
        pokemon_nature = None
        if nature:
            pokemon_nature = PokemonNature(
                freq=nature.get("freq", 0),
                vitality=nature.get("vitality", 0),
                exp=nature.get("exp", 0),
                ingr=nature.get("ingr", 0),
                skill=nature.get("skill", 0)
            )
        
        # サブスキルデータの変換
        pokemon_sub_skill = None
        if sub_skill:
            pokemon_sub_skill = PokemonSubSkill(
                skill=sub_skill.get("skill", 0),
                speed=sub_skill.get("speed", 0),
                ingr=sub_skill.get("ingr", 0),
                exp=sub_skill.get("exp", 0),
                help_bonus=sub_skill.get("help_bonus", 0),
                berry=sub_skill.get("berry", 0),
                inventory=sub_skill.get("inventory", 0),
                skill_lv_up=sub_skill.get("skill_lv_up", 0)
            )
        
        return Pokemon(
            name=name,
            level=level,
            nature=pokemon_nature,
            sub_skill=pokemon_sub_skill,
            ribbon=ribbon,
            base_data=base_data
        )
    
    def get_default_pokemon(self, name: str) -> Pokemon:
        """デフォルト設定のポケモンを取得（レベル50）"""
        cache_key = f"{name}_default"
        
        if cache_key not in self._pokemon_cache:
            self._pokemon_cache[cache_key] = self.create_pokemon(name, level=50)
        
        return self._pokemon_cache[cache_key]
    
    def get_pokemon_base_info(self, name: str) -> Dict[str, Any]:
        """ポケモンの基本情報を取得"""
        if not self.is_valid_pokemon_name(name):
            raise ValueError(f"不明なポケモン名: {name}")
        
        pokemon_data = self._pokemon_data[name]
        
        return {
            "name": pokemon_data["display_name"],
            "species": pokemon_data.get("species", pokemon_data["display_name"]),
            "level": pokemon_data.get("level", 50),
            "kind": pokemon_data["kind"],
            "type": pokemon_data["type"],
            "frequency": pokemon_data["frequency"],
            "berry": pokemon_data["berry"],
            "berry_energy": pokemon_data.get("berry_energy", 0),
            "ingredients": pokemon_data["ingredients"],
            "main_skill": pokemon_data["main_skill"],
            "skill_probability": pokemon_data.get("skill_probability", 0.0),
            "ingredient_probability": pokemon_data.get("ingredient_probability", 0.0),
            "inventory_size": pokemon_data.get("inventory_size", 10),
            "nature": pokemon_data.get("nature", {}),
            "subskill": pokemon_data.get("subskill", {}),
            "main_skill_level": pokemon_data.get("main_skill_level", 1),
            "evolution_stage": pokemon_data.get("evolution_stage", 0),
            "vitality": pokemon_data.get("vitality", 100),
            "ribbon": pokemon_data.get("ribbon", "ABA")
        }
    
    def get_all_pokemon_info(self) -> List[Dict[str, Any]]:
        """全ポケモンの基本情報を取得"""
        return [self.get_pokemon_base_info(name) for name in self._available_pokemon]
    
    def get_pokemon_by_type(self, pokemon_type: str) -> List[str]:
        """指定タイプのポケモン名リストを取得"""
        result = []
        for name in self._available_pokemon:
            pokemon_data = self._pokemon_data[name]
            if pokemon_data["type"] == pokemon_type:
                result.append(name)
        return result
    
    def validate_party_composition(self, party_names: List[str]) -> Dict[str, Any]:
        """パーティ構成の妥当性をチェック"""
        errors = []
        warnings = []
        
        # ポケモン名の有効性チェック
        for name in party_names:
            if not self.is_valid_pokemon_name(name):
                errors.append(f"不明なポケモン名: {name}")
        
        # パーティサイズチェック
        if len(party_names) > 5:
            errors.append("パーティは最大5匹まで編成可能です")
        elif len(party_names) == 0:
            errors.append("パーティにポケモンが含まれていません")
        
        # 重複チェック
        if len(party_names) != len(set(party_names)):
            errors.append("同じポケモンが複数回選択されています")
        
        # タイプバランスチェック（警告）
        if not errors:
            type_counts = {"きのみ": 0, "食材": 0, "スキル": 0}
            for name in party_names:
                if name in self._pokemon_data:
                    pokemon_type = self._pokemon_data[name]["type"]
                    type_counts[pokemon_type] += 1
            
            if type_counts["食材"] == 0:
                warnings.append("食材タイプのポケモンがいません")
            if type_counts["スキル"] == 0:
                warnings.append("スキルタイプのポケモンがいません")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "type_distribution": self._get_type_distribution(party_names) if not errors else {}
        }
    
    def _get_type_distribution(self, party_names: List[str]) -> Dict[str, int]:
        """パーティのタイプ分布を計算"""
        type_counts = {"きのみ": 0, "食材": 0, "スキル": 0}
        for name in party_names:
            if self.is_valid_pokemon_name(name):
                pokemon_type = self._pokemon_data[name]["type"]
                type_counts[pokemon_type] += 1
        return type_counts
    
    def get_load_status(self) -> bool:
        """データ読み込み状況を取得"""
        return self._load_status
    
    def refresh_data(self) -> bool:
        """データを再読み込み"""
        try:
            # キャッシュをクリア
            self._pokemon_cache.clear()
            
            # 再度データを読み込み
            self._load_all_pokemon_data()
            
            if self._pokemon_data:
                logger.info(f"Pokemon data refreshed successfully: {len(self._available_pokemon)} pokemon available")
                return True
            else:
                logger.error("Failed to refresh pokemon data - no data loaded")
                return False
            
        except Exception as e:
            logger.error(f"Failed to refresh pokemon data: {e}")
            self._load_status = False
            return False


# グローバルインスタンス
pokemon_data_manager = PokemonDataManager()

# 初期化は__init__内で行われるため不要