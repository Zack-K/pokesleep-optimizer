"""
pokes.py データ変換モジュール
既存のPokemonインスタンスを新しいアーキテクチャに対応した形式に変換
"""
import sys
import os
from typing import Dict, Any, List
import logging

# プロジェクトルートを追加してpokes.pyをインポート
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, backend_root)

logger = logging.getLogger(__name__)


def load_pokes_data() -> Dict[str, Dict[str, Any]]:
    """
    pokes.pyからポケモンデータを安全に読み込み、
    新しいアーキテクチャ対応形式に変換
    """
    try:
        # 循環インポートを避けるため、ここで動的インポート
        from define import BERRY, FOOD
        
        # pokes.pyのPKSデータを読み込み
        import pokes
        PKS = pokes.PKS
        
        converted_data = {}
        
        for name, pokemon_instance in PKS.items():
            try:
                # Pokemonインスタンスから必要なデータを抽出
                converted_data[name] = {
                    "display_name": name,  # 表示名（ニックネーム）
                    "species": pokemon_instance.tribe,  # 種族名
                    "level": pokemon_instance.lv,
                    "kind": pokemon_instance.pokemon["kind"],
                    "type": pokemon_instance.pokemon["type"],
                    "frequency": pokemon_instance.pokemon["freq"],
                    "berry": pokemon_instance.pokemon["berry"],
                    "berry_energy": BERRY.get(pokemon_instance.pokemon["berry"], 0),
                    "ingredients": pokemon_instance.pokemon["ingr"],
                    "main_skill": pokemon_instance.pokemon["main_skill"],
                    "skill_probability": pokemon_instance.skill_prob,
                    "ingredient_probability": pokemon_instance.ingr_prob,
                    "inventory_size": pokemon_instance.inventory,
                    
                    # 詳細設定
                    "nature": {
                        "freq": pokemon_instance.nature.get("freq", 0),
                        "vitality": pokemon_instance.nature.get("vitality", 0),
                        "exp": pokemon_instance.nature.get("exp", 0),
                        "ingr": pokemon_instance.nature.get("ingr", 0),
                        "skill": pokemon_instance.nature.get("skill", 0),
                    },
                    
                    "subskill": extract_subskill_data(pokemon_instance.subskill),
                    
                    "main_skill_level": getattr(pokemon_instance, 'mainskill_lv', 1),
                    "evolution_stage": getattr(pokemon_instance, 'n_evolve', 0),
                    "vitality": getattr(pokemon_instance, 'vitality', 100),
                    "ribbon": getattr(pokemon_instance, 'ribbon', 'ABA'),
                }
                
            except Exception as e:
                logger.warning(f"Failed to convert pokemon {name}: {e}")
                continue
                
        logger.info(f"Successfully converted {len(converted_data)} pokemon from pokes.py")
        return converted_data
        
    except ImportError as e:
        logger.error(f"Failed to import pokes.py: {e}")
        return {}
    except Exception as e:
        logger.error(f"Failed to load pokes data: {e}")
        return {}


def extract_subskill_data(subskill_data: Dict[str, Any]) -> Dict[str, int]:
    """
    サブスキルデータを統一形式に変換
    """
    result = {
        "skill": 0,
        "speed": 0,
        "ingr": 0,
        "exp": 0,
        "help_bonus": 0,
        "berry": 0,
        "inventory": 0,
        "skill_lv_up": 0,
        "eng_bonus": 0,
    }
    
    for key, value in subskill_data.items():
        if key not in result:
            continue
            
        if isinstance(value, list):
            # リスト形式の場合は合計値を計算
            result[key] = sum(value) if value else 0
        elif isinstance(value, (int, float)):
            result[key] = int(value)
        else:
            result[key] = 0
            
    return result


def get_pokemon_types() -> List[str]:
    """利用可能なポケモンタイプ一覧を取得"""
    return ["きのみ", "食材", "スキル"]


def get_pokemon_species_list() -> List[str]:
    """利用可能な種族名一覧を取得"""
    try:
        import pokes
        species_set = set()
        for pokemon_instance in pokes.PKS.values():
            species_set.add(pokemon_instance.tribe)
        return sorted(list(species_set))
    except Exception as e:
        logger.error(f"Failed to get species list: {e}")
        return []


if __name__ == "__main__":
    # テスト実行
    logging.basicConfig(level=logging.INFO)
    data = load_pokes_data()
    print(f"Loaded {len(data)} pokemon")
    if data:
        first_pokemon = next(iter(data.values()))
        print(f"Sample pokemon: {first_pokemon}")