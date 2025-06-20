"""
ポケモンデータの定義
循環インポートを避けるため、pokemon_models.pyからPokemonクラスをインポート
"""
from pokemon_models import Pokemon

PKS = {
    "発電所": Pokemon("発電所", "ライチュウ", 61, "ABA", vitality=100, 
                    nature={"freq":1, "vitality":0, "exp":0, "ingr":0, "skill":-1}, 
                    subskill={"skill":0, "speed":[0,0,2], "ingr":0, "exp":0, "help_bonus":[0,0,0,0,1], "berry":[1,0,0], "skill_lv_up":[0,2,0], "inventory":0},
                    mainskill_lv=3,
                    n_evolve=2),
    "つよイーブイ": Pokemon("つよイーブイ", "エーフィ", 54, "ABB", vitality=100, 
                    nature={"freq":0, "vitality":-1, "exp":1, "ingr":0, "skill":0}, 
                    subskill={"skill":[0,2,0,0,0], "speed":[0,0,0,2,0], "ingr":[0,0,1,0,0], "exp": 0, "help_bonus":0, "berry":0, "skill_lv_up":[2,0,0,0,1], "inventory":0},
                    mainskill_lv=5,
                    n_evolve=1),
    "う　さ　ぎ": Pokemon("う　さ　ぎ", "カメックス", 60, "ABB", vitality=100, 
                    nature={"freq":0, "vitality":0, "exp":0, "ingr":0, "skill":0}, 
                    subskill={"skill":[0,0,0,1], "speed":2, "ingr":2, "exp":0, "help_bonus":0, "berry":0, "inventory":[0,0,1,0,2]},
                    mainskill_lv=3,
                    n_evolve=2),
    "卵白": Pokemon("卵白", "プクリン", 54, "ABA", vitality=100, 
                    nature={"freq":0, "vitality":1, "exp":0, "ingr":-1, "skill":0}, 
                    subskill={"skill":[0,0,2,1], "speed":[0,0,0,0,1], "ingr":0, "exp":0, "help_bonus":1, "berry":0, "inventory":0},
                    mainskill_lv=6,
                    n_evolve=2),
    "スイクン": Pokemon("スイクン", "スイクン", 25, "AAB", vitality=100, 
                nature={"freq":0, "vitality":1, "exp":0, "ingr":-1, "skill":0}, 
                subskill={"skill":2, "speed":2, "ingr":0, "exp": 0, "help_bonus":0, "berry":0, "inventory":0},
                mainskill_lv=6,
                n_evolve=0),
    # 他のポケモンも同様に追加可能
}

def get_all_pokemon():
    """全ポケモンのリストを取得"""
    return list(PKS.values())

def get_pokemon_by_name(name: str):
    """名前でポケモンを取得"""
    return PKS.get(name)

def get_pokemon_names():
    """ポケモン名のリストを取得"""
    return list(PKS.keys())