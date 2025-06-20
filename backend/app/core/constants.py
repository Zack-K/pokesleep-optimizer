"""
ゲーム定数の定義
循環インポートを避けるため、定数のみを定義
"""
from typing import Dict, Any

# ポケモンタイプ定数
PK_NORMAL = 1
PK_FIRE = 2
PK_WATER = 3
PK_ELECTRIC = 4
PK_GRASS = 5
PK_ICE = 6
PK_FIGHTER = 7
PK_POISON = 8
PK_GROUND = 9
PK_FLY = 10
PK_ESP = 11
PK_INSECT = 12
PK_ROCK = 13
PK_GHOST = 14
PK_DRAGON = 15
PK_AKU = 16
PK_METAL = 17
PK_FAIRY = 18

# レシピタイプ
ID_RECIPE_CURRY = 1
ID_RECIPE_SALAD = 2
ID_RECIPE_DEZERT = 3

# メインスキル定数
MS_CHARGE_STRENGTH_S = 1
MS_CHARGE_STRENGTH_M = 2
MS_DREAM_SHARD_MAGNET_S = 3
MS_ENERGIZING_CHEER_S = 4
MS_ENERGY_CHARGE_S = 5
MS_ENERGY_4_EVERYONE = 6
MS_EXTRA_HELPFUL_S = 7
MS_INGREDIENT_MAGNET_S = 8
MS_COOKING_POWER_UP_S = 9
MS_METRONOME = 10
MS_TASTY_CHANCE = 11
MS_HELPER_BOOST = 12

# その他の定数
COOKING_SUCCESSFUL_RATE = 0.1
COOKING_SUCCESSFUL_FACT = 2
GCT = False  # Good Camp Ticket
FORCE_RECIPE_LV = 60
FORCE_PK_LV = None

# ゲーム内データ（簡略版）
BERRY: Dict[str, int] = {
    "オレンのみ": 31,
    "オボンのみ": 43,
    "ヒメリのみ": 33,
    "フィラのみ": 40,
    "ウイのみ": 43,
    "マゴのみ": 40,
    "バンジのみ": 43,
    "イアのみ": 40,
    "ラムのみ": 34,
    "シーヤのみ": 33,
    "カゴのみ": 31,
    "ウブのみ": 24,
    "ドリのみ": 35,
    "ベリブのみ": 33,
    "ヤチェのみ": 35,
    "クラボのみ": 27,
    "カムラのみ": 29,
    "ヨプのみ": 30,
    "ザロクのみ": 22,
    "チーゴのみ": 30,
}

FOOD: Dict[str, int] = {
    "ミルク": 98,
    "エッグ": 115,
    "リンゴ": 90,
    "ミツ": 101,
    "オイル": 121,
    "ハーブ": 101,
    "コーン": 140,
    "ポテト": 124,
    "大豆": 100,
    "ジンジャー": 109,
    "トマト": 110,
    "カカオ": 151,
    "ながねぎ": 109,
    "シッポ": 109,
    "キノコ": 167,
    "ミート": 103,
    "コーヒー": 145,
}

# ポケモン基本データ（サンプル）
POKEMON_BASE_DATA: Dict[str, Dict[str, Any]] = {
    "ライチュウ": {
        "kind": PK_ELECTRIC,
        "type": "スキル",
        "freq": 2300,
        "berry": "ウブのみ",
        "ingr": ["リンゴ", "エッグ", "ハーブ"],
        "main_skill": MS_CHARGE_STRENGTH_S,
    },
    "エーフィ": {
        "kind": PK_ESP,
        "type": "スキル", 
        "freq": 3300,
        "berry": "マゴのみ",
        "ingr": ["ミルク", "大豆", "カカオ"],
        "main_skill": MS_CHARGE_STRENGTH_S,
    },
    "カメックス": {
        "kind": PK_WATER,
        "type": "食材",
        "freq": 4400,
        "berry": "オレンのみ",
        "ingr": ["ミルク", "トマト", "ポテト"],
        "main_skill": MS_EXTRA_HELPFUL_S,
    },
    "プクリン": {
        "kind": PK_NORMAL,
        "type": "きのみ",
        "freq": 2700,
        "berry": "オレンのみ",
        "ingr": ["エッグ", "リンゴ", "ミルク"],
        "main_skill": MS_ENERGY_4_EVERYONE,
    },
    "スイクン": {
        "kind": PK_WATER,
        "type": "スキル",
        "freq": 4200,
        "berry": "オボンのみ", 
        "ingr": ["大豆", "コーン", "ジンジャー"],
        "main_skill": MS_ENERGY_4_EVERYONE,
    },
}

# 確率データ（サンプル）
PROBABILITY: Dict[str, Dict[str, float]] = {
    "ライチュウ": {"skill": 18.8, "ingr": 17.6},
    "エーフィ": {"skill": 19.8, "ingr": 17.7},
    "カメックス": {"skill": 6.9, "ingr": 23.4},
    "プクリン": {"skill": 4.9, "ingr": 13.6},
    "スイクン": {"skill": 4.4, "ingr": 11.6},
}

# インベントリサイズ
INVENTORY: Dict[str, int] = {
    "ライチュウ": 18,
    "エーフィ": 14,
    "カメックス": 17,
    "プクリン": 15,
    "スイクン": 20,
}

# イベントボーナス設定
EVENT_BONUS_RECIPE_FACT = 1.0
EVENT_BONUS_SKILL_TRIGGER = {"kind": [], "type": [], "fact": 1.0}
EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [], "type": [], "amount": 0}
EVENT_BONUS_SKILL_LV_UP = {"kind": [], "type": [], "amount": 0}
EVENT_BONUS_VITALITY_RECOV_AMOUNT = 0

# レシピレベルボーナステーブル
RECIPE_LV_BONUS_TABLE = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]

# フィールドきのみ設定
FIELD_BERRY_NONE = []
FIELD_BERRY_WAKAKUSA = ["オレンのみ"]
FIELD_BERRY_CYAN = ["オボンのみ"] 
FIELD_BERRY_TAUPE = ["ヒメリのみ"]
FIELD_BERRY_SNOWDROP = ["ウブのみ"]
FIELD_BERRY_LAPIS = ["マゴのみ"]
FIELD_BERRY_OGPP = ["ヤチェのみ"]