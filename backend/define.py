## PK type indices
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

# list_up_possible_recipeにおいて考慮するレシピ数を制限できる。単純ホワイトシチューなどを目的に食材確保がされることを避けたいときに使用
MAX_N_RECIPE_CONSIDER = 1
# choose_additional_ingredients2において、non_essentials以外の食材の使用時に最低これだけの食材数は残す数
N_SAVE_ESSENTIAL = 15

#### EVENT ####
EVENT_BONUS_RECIPE_FACT = 1.0
EVENT_BONUS_SKILL_TRIGGER = {"kind": [], "type":[], "fact":1.5}
EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [], "type":[], "amount":1}
EVENT_BONUS_SKILL_LV_UP = {"kind": [], "type":[], "amount":1}
EVENT_BONUS_VITALITY_RECOV_AMOUNT = 0
# """ suicune research """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_WATER], "fact":1.5}
# EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [PK_WATER], "amount":1}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [PK_WATER], "amount":3}
""" HW event """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_GHOST], "fact":1.5}
# EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [PK_GHOST], "amount":1}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [PK_GHOST], "amount":1}
""" EV week """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_NORMAL,PK_FIRE,PK_WATER,PK_ELECTRIC,PK_GRASS,PK_ICE,PK_FIGHTER,PK_POISON,PK_GROUND,PK_FLY,PK_ESP,PK_INSECT,PK_ROCK,PK_GHOST,PK_DRAGON,PK_AKU,PK_METAL,PK_FAIRY], "fact":1.5}
""" holiday week """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_ICE], "fact":1.5}
# EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [PK_ICE], "amount":1}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [PK_ICE], "amount":1}
""" new year """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_NORMAL,PK_FIRE,PK_WATER,PK_ELECTRIC,PK_GRASS,PK_ICE,PK_FIGHTER,PK_POISON,PK_GROUND,PK_FLY,PK_ESP,PK_INSECT,PK_ROCK,PK_GHOST,PK_DRAGON,PK_AKU,PK_METAL,PK_FAIRY], "fact":1.25}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [PK_NORMAL,PK_FIRE,PK_WATER,PK_ELECTRIC,PK_GRASS,PK_ICE,PK_FIGHTER,PK_POISON,PK_GROUND,PK_FLY,PK_ESP,PK_INSECT,PK_ROCK,PK_GHOST,PK_DRAGON,PK_AKU,PK_METAL,PK_FAIRY], "amount":1}
# EVENT_BONUS_RECIPE_FACT = 1.25
""" skill type week """
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [], "type":["スキル"], "fact":1.5}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [], "type":["スキル"], "amount":3}
""" 214 campaign """
# EVENT_BONUS_RECIPE_FACT = 1.5
"""クレセリア"""
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_ESP], "type":[], "fact":1.5}
# EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [PK_ESP], "type":[], "amount":1}
# EVENT_BONUS_SKILL_LV_UP = {"kind": [PK_ESP], "type":[], "amount":3}
"""ゆめのかけらget week"""
# EVENT_BONUS_SKILL_TRIGGER = {"kind": [PK_NORMAL,PK_FIRE,PK_WATER,PK_ELECTRIC,PK_GRASS,PK_ICE,PK_FIGHTER,PK_POISON,PK_GROUND,PK_FLY,PK_ESP,PK_INSECT,PK_ROCK,PK_GHOST,PK_DRAGON,PK_AKU,PK_METAL,PK_FAIRY], "type":[], "fact":1.25}
"""デカ盛り week"""
# EVENT_BONUS_ADDITIONAL_INGREDIENT = {"kind": [], "type":["食材"], "amount":1}
# EVENT_BONUS_RECIPE_FACT = 1.5
# EVENT_BONUS_VITALITY_RECOV_AMOUNT = 5


COOKING_SUCCESSFUL_RATE = 0.1
COOKING_SUCCESSFUL_FACT= 2

#### GOOD CAMP TICKET ###
GCT = True
GCT = False

# update 2024/8
ENABLE_SKILL_DOUBLE_STANDBY = True

# 
FORCE_RECIPE_LV = 60
FORCE_PK_LV = 0

## LOG LEVEL ##
# LOG_LEVEL = 4

## main skill indices ##
MS_CHARGE_STRENGTH_S = 1
MS_CHARGE_STRENGTH_S_RANDOM = 13
MS_CHARGE_STRENGTH_M = 2
MS_DREAM_SHARD_MAGNET_S = 3
MS_DREAM_SHARD_MAGNET_S_RANDOM = 14
MS_ENERGIZING_CHEER_S = 4
MS_ENERGY_CHARGE_S = 5
MS_ENERGY_4_EVERYONE = 6
MS_EXTRA_HELPFUL_S = 7
MS_INGREDIENT_MAGNET_S = 8
MS_COOKING_POWER_UP_S = 9
MS_METRONOME = 10
MS_TASTY_CHANCE = 11
MS_HELPER_BOOST = 12
MS_CHARGE_STRENGTH_ACCUM = 15
MS_ENERGY_CHARGE_MOONLIGHT= 16
MS_ENERGY_CHARGE_MOONLIGHT_SUCCESS_PROB = 0.45 # つきのひかり大成功確率(0-1)
MS_BERRY_BURST= 17
MS_BERRY_BURST_SUCCESS_PROB = 0.2 # 大成功確率(0-1)
MS_SKILL_COPY= 18
MS_LUNAR_BRESSING = 19
MS_NIGHTMARE = 20
N_KIND_MS = 20 #スキルの個数 (ゆびをふるの発動時に参照)


## field berry ##
FIELD_BERRY_CYAN = ["オレン", "シーヤ", "モモン"]
FIELD_BERRY_TAUPE = ["フィラ", "ヒメリ", "オボン"]
FIELD_BERRY_SNOWDROP = ["チーゴ", "ウイ", "キー"]
# FIELD_BERRY_WAKAKUSA = ["オレン", "チーゴ", "ヒメリ"]
# FIELD_BERRY_WAKAKUSA = ["チーゴ"]
FIELD_BERRY_WAKAKUSA = ["マゴ", "クラボ", "ブリー"]
# FIELD_BERRY_WAKAKUSA = ["シーヤ", "マゴ", "チーゴ"]
FIELD_BERRY_LAPIS = ["ドリ","クラボ","マゴ"]
FIELD_BERRY_OGPP = ["ウブ","ブリー","ベリブ"]
FIELD_BERRY_NONE = []


BERRY = {"キー":28, # snowdrop
        "ヒメリ":27, # taupe
        "オレン":31, # cyan
        "ウブ":25, # ogpp
        "ドリ":30, # lapis
        "チーゴ":32, # snowdrop
        "クラボ":27, # laps
        "カゴ":32, 
        "フィラ":29, # taupe
        "シーヤ":24, # cyan
        "マゴ":26, # lapis
        "ラム":24, 
        "オボン":30, # taupe
        "ブリー":26, # ogpp
        "ヤチェ":35, 
        "ウイ":31, # snowdrop
        "ベリブ":33, # ogpp
        "モモン":26, # cyan
        }

FOOD = {
        "シッポ": 342,
        "ながねぎ": 185,
        "キノコ": 167,
        "コーヒー": 153,
        "カカオ": 151,
        "コーン": 140,
        "ハーブ": 130,
        "ポテト": 124,
        "オイル": 121,
        "エッグ": 115,
        "トマト": 110,
        "ジンジャー": 109,
        "ミート": 103,
        "ミツ": 101,
        "大豆": 100,
        "ミルク": 98,
        "リンゴ": 90,
        }

POKEMON = {
        "フシギダネ":{"id":1, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["ミツ", "トマト", "ポテト"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":4400},
        "フシギソウ":{"id":2, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["ミツ", "トマト", "ポテト"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":12, "freq":3300},
        "フシギバナ":{"id":3, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["ミツ", "トマト", "ポテト"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":2800},
        "キャタピー":{"id":10, "kind":PK_INSECT, "type":"きのみ", "berry":"ラム", "ingr":["ミツ", "トマト", "大豆"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":4400},
        "トランセル":{"id":11, "kind":PK_INSECT, "type":"きのみ", "berry":"ラム", "ingr":["ミツ", "トマト", "大豆"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":7, "freq":4200},
        "バタフリー":{"id":12, "kind":PK_INSECT, "type":"きのみ", "berry":"ラム", "ingr":["ミツ", "トマト", "大豆"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":15, "freq":2600},
        "アーボ":{"id":23, "kind":PK_POISON, "type":"きのみ", "berry":"カゴ", "ingr":["ミート", "エッグ", "ハーブ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":5000},
        "アーボック":{"id":24, "kind":PK_POISON, "type":"きのみ", "berry":"カゴ", "ingr":["ミート", "エッグ", "ハーブ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3400},
        "コダック":{"id":54, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["カカオ", "リンゴ", "ミート"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":5400},
        "マンキー":{"id":56, "kind":PK_FIGHTER, "type":"きのみ", "berry":"クラボ", "ingr":["ミート", "キノコ", "ミツ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":4200},
        "オコリザル":{"id":57, "kind":PK_FIGHTER, "type":"きのみ", "berry":"クラボ", "ingr":["ミート", "キノコ", "ミツ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":2800},
        "マダツボミ":{"id":69, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["トマト", "ポテト", "ながねぎ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":5200},
        "ウツドン":{"id":70, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["トマト", "ポテト", "ながねぎ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3800},
        "ウツボット":{"id":71, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["トマト", "ポテト", "ながねぎ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":20, "freq":2800},
        "ゴース":{"id":92, "kind":PK_GHOST, "type":"食材", "berry":"ブリー", "ingr":["ハーブ", "キノコ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":3800},
        "ゴースト":{"id":93, "kind":PK_GHOST, "type":"食材", "berry":"ブリー", "ingr":["ハーブ", "キノコ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3000},
        "ゲンガー":{"id":94, "kind":PK_GHOST, "type":"食材", "berry":"ブリー", "ingr":["ハーブ", "キノコ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":22, "freq":2200},
        "カイロス":{"id":127, "kind":PK_INSECT, "type":"食材", "berry":"ラム", "ingr":["ミツ", "リンゴ", "ミート"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":16, "freq":2400},
        "ミニリュウ":{"id":147, "kind":PK_DRAGON, "type":"食材", "berry":"ヤチェ", "ingr":["ハーブ", "コーン", "オイル"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":5000},
        "ハクリュー":{"id":148, "kind":PK_DRAGON, "type":"食材", "berry":"ヤチェ", "ingr":["ハーブ", "コーン", "オイル"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3800},
        "カイリュー":{"id":149, "kind":PK_DRAGON, "type":"食材", "berry":"ヤチェ", "ingr":["ハーブ", "コーン", "オイル"], "main_skill":MS_ENERGY_CHARGE_S, "fp":25, "freq":2600},
        "チコリータ":{"id":152, "kind":PK_GRASS, "type":"きのみ", "berry":"ドリ", "ingr":["カカオ", "ミツ", "ながねぎ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":4400},
        "ベイリーフ":{"id":153, "kind":PK_GRASS, "type":"きのみ", "berry":"ドリ", "ingr":["カカオ", "ミツ", "ながねぎ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3300},
        "メガニウム":{"id":154, "kind":PK_GRASS, "type":"きのみ", "berry":"ドリ", "ingr":["カカオ", "ミツ", "ながねぎ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":20, "freq":2800},
        "ブラッキー":{"id":197, "kind":PK_AKU, "type":"スキル", "berry":"ウイ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_ENERGY_CHARGE_MOONLIGHT, "fp":20, "freq":3200},
        "ヘラクロス":{"id":214, "kind":PK_INSECT, "type":"スキル", "berry":"ラム", "ingr":["ミツ", "キノコ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":16, "freq":2300},
        "デリバード":{"id":225, "kind":PK_FLY, "type":"食材", "berry":"シーヤ", "ingr":["エッグ", "リンゴ", "カカオ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":16, "freq":2500},
        "デルビル":{"id":228, "kind":PK_AKU, "type":"きのみ", "berry":"ウイ", "ingr":["ハーブ", "ジンジャー", "ながねぎ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":5, "freq":4900},
        "ヘルガー":{"id":229, "kind":PK_AKU, "type":"きのみ", "berry":"ウイ", "ingr":["ハーブ", "ジンジャー", "ながねぎ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":12, "freq":3300},
        "バンギラス":{"id":248, "kind":PK_AKU, "type":"食材", "berry":"ウイ", "ingr":["ジンジャー", "大豆", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":25, "freq":2700},
        "ヤルキモノ":{"id":288, "kind":PK_NORMAL, "type":"きのみ", "berry":"キー", "ingr":["トマト", "ミツ", "リンゴ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":12, "freq":3200},
        "ヤミラミ":{"id":302, "kind":PK_AKU, "type":"スキル", "berry":"ウイ", "ingr":["オイル", "キノコ", "カカオ"], "main_skill":MS_DREAM_SHARD_MAGNET_S_RANDOM, "fp":16, "freq":3600},
        "ゴクリン":{"id":316, "kind":PK_POISON, "type":"スキル", "berry":"カゴ", "ingr":["大豆", "キノコ", "ミツ"], "main_skill":MS_DREAM_SHARD_MAGNET_S_RANDOM, "fp":5, "freq":5900},
        "マルノーム":{"id":317, "kind":PK_POISON, "type":"スキル", "berry":"カゴ", "ingr":["大豆", "キノコ", "ミツ"], "main_skill":MS_DREAM_SHARD_MAGNET_S_RANDOM, "fp":12, "freq":3500},
        "チルタリス":{"id":334, "kind":PK_DRAGON, "type":"きのみ", "berry":"ヤチェ", "ingr":["エッグ", "大豆", "リンゴ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3700},
        "カゲボウズ":{"id":353, "kind":PK_GHOST, "type":"きのみ", "berry":"ブリー", "ingr":["オイル", "ジンジャー", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":3900},
        "ジュペッタ":{"id":354, "kind":PK_GHOST, "type":"きのみ", "berry":"ブリー", "ingr":["オイル", "ジンジャー", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":16, "freq":2600},
        "アブソル":{"id":359, "kind":PK_AKU, "type":"食材", "berry":"ウイ", "ingr":["カカオ", "リンゴ", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":16, "freq":2950},
        "グレッグル":{"id":453, "kind":PK_POISON, "type":"食材", "berry":"カゴ", "ingr":["オイル", "ミート", ""], "main_skill":MS_CHARGE_STRENGTH_S, "fp":"", "freq":5, "freq":5600},
        "ドクロッグ":{"id":454, "kind":PK_POISON, "type":"食材", "berry":"カゴ", "ingr":["オイル", "ミート", ""], "main_skill":MS_CHARGE_STRENGTH_S, "fp":"", "freq":12, "freq":3400},
        "リーフィア":{"id":470, "kind":PK_GRASS, "type":"スキル", "berry":"ドリ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":20, "freq":3000},
        "ヒトカゲ":{"id":4, "kind":PK_FIRE, "type":"食材", "berry":"ヒメリ", "ingr":["ミート", "ジンジャー", "ハーブ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":3500},
        "リザード":{"id":5, "kind":PK_FIRE, "type":"食材", "berry":"ヒメリ", "ingr":["ミート", "ジンジャー", "ハーブ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":12, "freq":3000},
        "リザードン":{"id":6, "kind":PK_FIRE, "type":"食材", "berry":"ヒメリ", "ingr":["ミート", "ジンジャー", "ハーブ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":2400},
        "コラッタ":{"id":19, "kind":PK_NORMAL, "type":"きのみ", "berry":"キー", "ingr":["リンゴ", "大豆", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":4900},
        "ラッタ":{"id":20, "kind":PK_NORMAL, "type":"きのみ", "berry":"キー", "ingr":["リンゴ", "大豆", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":2950},
        "ピカチュウ":{"id":25, "kind":PK_ELECTRIC, "type":"きのみ", "berry":"ウブ", "ingr":["リンゴ", "ジンジャー", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":7, "freq":2700},
        "ピカチュウハロウィン":{"id":25, "kind":PK_ELECTRIC, "type":"きのみ", "berry":"ウブ", "ingr":["リンゴ", "ジンジャー", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":7, "freq":2500},
        "ピカチュウホリデー":{"id":25, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["リンゴ", "ジンジャー", "エッグ"], "main_skill":MS_DREAM_SHARD_MAGNET_S, "fp":7, "freq":2500},
        "ライチュウ":{"id":26, "kind":PK_ELECTRIC, "type":"きのみ", "berry":"ウブ", "ingr":["リンゴ", "ジンジャー", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":18, "freq":2200},
        "ピッピ":{"id":35, "kind":PK_FAIRY, "type":"きのみ", "berry":"モモン", "ingr":["リンゴ", "ミツ", "大豆"], "main_skill":MS_METRONOME, "fp":7, "freq":4000},
        "ピクシー":{"id":36, "kind":PK_FAIRY, "type":"きのみ", "berry":"モモン", "ingr":["リンゴ", "ミツ", "大豆"], "main_skill":MS_METRONOME, "fp":20, "freq":2800},
        "ロコン":{"id":37, "kind":PK_FIRE, "type":"きのみ", "berry":"ヒメリ", "ingr":["大豆", "コーン", "ポテト"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":5, "freq":4700},
        "キュウコン":{"id":38, "kind":PK_FIRE, "type":"きのみ", "berry":"ヒメリ", "ingr":["大豆", "コーン", "ポテト"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":20, "freq":2600},
        "プリン":{"id":39, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["ミツ", "オイル", "カカオ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":7, "freq":3900},
        "プクリン":{"id":40, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["ミツ", "オイル", "カカオ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":16, "freq":2900},
        "ディグダ":{"id":50, "kind":PK_GROUND, "type":"食材", "berry":"フィラ", "ingr":["トマト", "ながねぎ", "大豆"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":5, "freq":4300},
        "ダグトリオ":{"id":51, "kind":PK_GROUND, "type":"食材", "berry":"フィラ", "ingr":["トマト", "ながねぎ", "大豆"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":12, "freq":2800},
        "ニャース":{"id":52, "kind":PK_NORMAL, "type":"スキル", "berry":"キー", "ingr":["ミルク", "ミート", ""], "main_skill":MS_DREAM_SHARD_MAGNET_S, "fp":5, "freq":4400},
        "ペルシアン":{"id":53, "kind":PK_NORMAL, "type":"スキル", "berry":"キー", "ingr":["ミルク", "ミート", ""], "main_skill":MS_DREAM_SHARD_MAGNET_S, "fp":12, "freq":2800},
        "ガーディ":{"id":58, "kind":PK_FIRE, "type":"スキル", "berry":"ヒメリ", "ingr":["ハーブ", "ミート", "ミルク"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":5, "freq":4300},
        "ウインディ":{"id":59, "kind":PK_FIRE, "type":"スキル", "berry":"ヒメリ", "ingr":["ハーブ", "ミート", "ミルク"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":20, "freq":2500},
        "ヤドン":{"id":79, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["カカオ", "シッポ", "トマト"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":5, "freq":5700},
        "ヤドラン":{"id":80, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["カカオ", "シッポ", "トマト"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":12, "freq":3800},
        "ガルーラ":{"id":115, "kind":PK_NORMAL, "type":"食材", "berry":"キー", "ingr":["ジンジャー", "ポテト", "大豆"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":16, "freq":2650},
        "バリヤード":{"id":122, "kind":PK_ESP, "type":"食材", "berry":"マゴ", "ingr":["トマト", "ポテト", "ながねぎ"], "main_skill":MS_SKILL_COPY, "fp":12, "freq":2800},
        "メタモン":{"id":132, "kind":PK_NORMAL, "type":"食材", "berry":"キー", "ingr":["オイル", "ながねぎ", "シッポ"], "main_skill":MS_SKILL_COPY, "fp":16, "freq":3500},
        "イーブイ":{"id":133, "kind":PK_NORMAL, "type":"スキル", "berry":"キー", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":3700},
        "サンダース":{"id":135, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":20, "freq":2200},
        "ブースター":{"id":136, "kind":PK_FIRE, "type":"スキル", "berry":"ヒメリ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_COOKING_POWER_UP_S, "fp":20, "freq":2700},
        "ヒノアラシ":{"id":155, "kind":PK_FIRE, "type":"きのみ", "berry":"ヒメリ", "ingr":["ジンジャー", "ハーブ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":3500},
        "マグマラシ":{"id":156, "kind":PK_FIRE, "type":"きのみ", "berry":"ヒメリ", "ingr":["ジンジャー", "ハーブ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3000},
        "バクフーン":{"id":157, "kind":PK_FIRE, "type":"きのみ", "berry":"ヒメリ", "ingr":["ジンジャー", "ハーブ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":20, "freq":2400},
        "トゲチック":{"id":176, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["エッグ", "ジンジャー", "カカオ"], "main_skill":MS_METRONOME, "fp":12, "freq":3800},
        "メリープ":{"id":179, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["ハーブ", "エッグ", ""], "main_skill":MS_CHARGE_STRENGTH_M, "fp":5, "freq":4600},
        "モココ":{"id":180, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["ハーブ", "エッグ", ""], "main_skill":MS_CHARGE_STRENGTH_M, "fp":12, "freq":3300},
        "デンリュウ":{"id":181, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["ハーブ", "エッグ", ""], "main_skill":MS_CHARGE_STRENGTH_M, "fp":20, "freq":2500},
        "エーフィ":{"id":196, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":20, "freq":2400},
        "ヤドキング":{"id":199, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["カカオ", "シッポ", "トマト"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":20, "freq":3400},
        "ソーナンス":{"id":202, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["リンゴ", "キノコ", "オイル"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":7, "freq":3500},
        "ライコウ":{"id":243, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["ミート", "ハーブ", "ながねぎ"], "main_skill":MS_HELPER_BOOST, "fp":30, "freq":2100},
        "エンテイ":{"id":244, "kind":PK_FIRE, "type":"スキル", "berry":"ヒメリ", "ingr":["オイル", "トマト", "キノコ"], "main_skill":MS_HELPER_BOOST, "fp":30, "freq":2400},
        "スイクン":{"id":245, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["リンゴ", "オイル", "コーン"], "main_skill":MS_HELPER_BOOST, "fp":30, "freq":2700},
        "ラルトス":{"id":280, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["リンゴ", "コーン", "ながねぎ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":5, "freq":4800},
        "キルリア":{"id":281, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["リンゴ", "コーン", "ながねぎ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":12, "freq":3500},
        "サーナイト":{"id":282, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["リンゴ", "コーン", "ながねぎ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":20, "freq":2400},
        "ナマケロ":{"id":287, "kind":PK_NORMAL, "type":"きのみ", "berry":"キー", "ingr":["トマト", "ミツ", "リンゴ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":4900},
        "ケッキング":{"id":289, "kind":PK_NORMAL, "type":"きのみ", "berry":"キー", "ingr":["トマト", "ミツ", "リンゴ"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":22, "freq":3600},
        "トゲキッス":{"id":468, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["エッグ", "ジンジャー", "カカオ"], "main_skill":MS_METRONOME, "fp":22, "freq":2600},
        "ニンフィア":{"id":700, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":20, "freq":2600},
        "デデンネ":{"id":702, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["リンゴ", "カカオ", "コーン"], "main_skill":MS_TASTY_CHANCE, "fp":16, "freq":2500},
        "キュワワー":{"id":764, "kind":PK_FAIRY, "type":"食材", "berry":"モモン", "ingr":["コーン", "ジンジャー", "カカオ"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":16, "freq":2500},
        "ゼニガメ":{"id":7, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":4500},
        "カメール":{"id":8, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":12, "freq":3400},
        "カメックス":{"id":9, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":2800},
        "ゴルダック":{"id":55, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["カカオ", "リンゴ", "ミート"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3400},
        "イシツブテ":{"id":74, "kind":PK_ROCK, "type":"食材", "berry":"オボン", "ingr":["大豆", "ポテト", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":5700},
        "ゴローン":{"id":75, "kind":PK_ROCK, "type":"食材", "berry":"オボン", "ingr":["大豆", "ポテト", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":4000},
        "ゴローニャ":{"id":76, "kind":PK_ROCK, "type":"食材", "berry":"オボン", "ingr":["大豆", "ポテト", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":22, "freq":3100},
        "コイル":{"id":81, "kind":PK_METAL, "type":"スキル", "berry":"ベリブ", "ingr":["オイル", "ハーブ", ""], "main_skill":MS_COOKING_POWER_UP_S, "fp":5, "freq":5800},
        "レアコイル":{"id":82, "kind":PK_METAL, "type":"スキル", "berry":"ベリブ", "ingr":["オイル", "ハーブ", ""], "main_skill":MS_COOKING_POWER_UP_S, "fp":12, "freq":4000},
        "ドードー":{"id":84, "kind":PK_FLY, "type":"きのみ", "berry":"シーヤ", "ingr":["大豆", "カカオ", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":3800},
        "ドードリオ":{"id":85, "kind":PK_FLY, "type":"きのみ", "berry":"シーヤ", "ingr":["大豆", "カカオ", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":2400},
        "イワーク":{"id":95, "kind":PK_ROCK, "type":"きのみ", "berry":"オボン", "ingr":["トマト", "ミート", "ポテト"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":16, "freq":3100},
        "カラカラ":{"id":104, "kind":PK_GROUND, "type":"きのみ", "berry":"フィラ", "ingr":["ジンジャー", "カカオ", ""], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":4800},
        "ガラガラ":{"id":105, "kind":PK_GROUND, "type":"きのみ", "berry":"フィラ", "ingr":["ジンジャー", "カカオ", ""], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3500},
        "シャワーズ":{"id":134, "kind":PK_WATER, "type":"スキル", "berry":"オレン", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":3100},
        "ワニノコ":{"id":158, "kind":PK_WATER, "type":"きのみ", "berry":"オレン", "ingr":["ミート", "オイル", ""], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":4500},
        "アリゲイツ":{"id":159, "kind":PK_WATER, "type":"きのみ", "berry":"オレン", "ingr":["ミート", "オイル", ""], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3400},
        "オーダイル":{"id":160, "kind":PK_WATER, "type":"きのみ", "berry":"オレン", "ingr":["ミート", "オイル", ""], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":20, "freq":2800},
        "ピチュー":{"id":172, "kind":PK_ELECTRIC, "type":"きのみ", "berry":"ウブ", "ingr":["リンゴ", "ジンジャー", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":5, "freq":4300},
        "ピィ":{"id":173, "kind":PK_FAIRY, "type":"きのみ", "berry":"モモン", "ingr":["リンゴ", "ミツ", "大豆"], "main_skill":MS_METRONOME, "fp":5, "freq":5600},
        "ププリン":{"id":174, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["ミツ", "オイル", "カカオ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":5, "freq":5200},
        "トゲピー":{"id":175, "kind":PK_FAIRY, "type":"スキル", "berry":"モモン", "ingr":["エッグ", "ジンジャー", "カカオ"], "main_skill":MS_METRONOME, "fp":5, "freq":4800},
        "ウソッキー":{"id":185, "kind":PK_ROCK, "type":"スキル", "berry":"オボン", "ingr":["トマト", "大豆", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":7, "freq":4000},
        "ハガネール":{"id":208, "kind":PK_METAL, "type":"きのみ", "berry":"ベリブ", "ingr":["トマト", "ミート", "ポテト"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":3000},
        "ヨーギラス":{"id":246, "kind":PK_ROCK, "type":"食材", "berry":"オボン", "ingr":["ジンジャー", "大豆", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":4800},
        "サナギラス":{"id":247, "kind":PK_ROCK, "type":"食材", "berry":"オボン", "ingr":["ジンジャー", "大豆", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3600},
        "チルット":{"id":333, "kind":PK_FLY, "type":"きのみ", "berry":"シーヤ", "ingr":["エッグ", "大豆", "リンゴ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":4200},
        "ソーナノ":{"id":360, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["リンゴ", "キノコ", "オイル"], "main_skill":MS_ENERGIZING_CHEER_S, "fp":5, "freq":5800},
        "タマザラシ":{"id":363, "kind":PK_ICE, "type":"きのみ", "berry":"チーゴ", "ingr":["オイル", "ミート", "ジンジャー"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":5, "freq":5600},
        "トドグラー":{"id":364, "kind":PK_ICE, "type":"きのみ", "berry":"チーゴ", "ingr":["オイル", "ミート", "ジンジャー"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":12, "freq":4000},
        "トドゼルガ":{"id":365, "kind":PK_ICE, "type":"きのみ", "berry":"チーゴ", "ingr":["オイル", "ミート", "ジンジャー"], "main_skill":MS_INGREDIENT_MAGNET_S, "fp":20, "freq":3000},
        "ウソハチ":{"id":438, "kind":PK_ROCK, "type":"スキル", "berry":"オボン", "ingr":["トマト", "大豆", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":5, "freq":6300},
        "マネネ":{"id":439, "kind":PK_ESP, "type":"食材", "berry":"マゴ", "ingr":["トマト", "ポテト", "ながねぎ"], "main_skill":MS_SKILL_COPY, "fp":5, "freq":4300},
        "リオル":{"id":447, "kind":PK_FIGHTER, "type":"スキル", "berry":"クラボ", "ingr":["オイル", "ポテト", "エッグ"], "main_skill":MS_DREAM_SHARD_MAGNET_S, "fp":5, "freq":4200},
        "ルカリオ":{"id":448, "kind":PK_FIGHTER, "type":"スキル", "berry":"クラボ", "ingr":["オイル", "ポテト", "エッグ"], "main_skill":MS_DREAM_SHARD_MAGNET_S, "fp":20, "freq":2600},
        "ユキカブリ":{"id":459, "kind":PK_ICE, "type":"食材", "berry":"チーゴ", "ingr":["トマト", "エッグ", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":5600},
        "ユキノオー":{"id":460, "kind":PK_ICE, "type":"食材", "berry":"チーゴ", "ingr":["トマト", "エッグ", "キノコ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":3000},
        "ジバコイル":{"id":462, "kind":PK_METAL, "type":"スキル", "berry":"ベリブ", "ingr":["オイル", "ハーブ", ""], "main_skill":MS_COOKING_POWER_UP_S, "fp":22, "freq":3100},
        "グレイシア":{"id":471, "kind":PK_ICE, "type":"スキル", "berry":"チーゴ", "ingr":["ミルク", "カカオ", "ミート"], "main_skill":MS_COOKING_POWER_UP_S, "fp":20, "freq":3200},
        "ムンナ":{"id":517, "kind":PK_ESP, "type":"きのみ", "berry":"マゴ", "ingr":["ミルク", "ミツ", "コーヒー"], "main_skill":MS_DREAM_SHARD_MAGNET_S_RANDOM, "fp":5, "freq":5700},
        "ムシャーナ":{"id":518, "kind":PK_ESP, "type":"きのみ", "berry":"マゴ", "ingr":["ミルク", "ミツ", "コーヒー"], "main_skill":MS_DREAM_SHARD_MAGNET_S_RANDOM, "fp":20, "freq":2800},
        "エルレイド":{"id":475, "kind":PK_FIGHTER, "type":"スキル", "berry":"クラボ", "ingr":["リンゴ", "コーン", "ながねぎ"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":22, "freq":2400},
        "ヌイコグマ":{"id":759, "kind":PK_FIGHTER, "type":"食材", "berry":"クラボ", "ingr":["コーン", "ミート", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":5, "freq":4100},
        "キテルグマ":{"id":760, "kind":PK_FIGHTER, "type":"食材", "berry":"クラボ", "ingr":["コーン", "ミート", "エッグ"], "main_skill":MS_CHARGE_STRENGTH_S_RANDOM, "fp":12, "freq":2800},
        "ウッウ":{"id":845, "kind":PK_FLY, "type":"食材", "berry":"シーヤ", "ingr":["オイル", "ポテト", "エッグ"], "main_skill":MS_TASTY_CHANCE, "fp":16, "freq":2700},
        "クワッス":{"id":912, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["大豆", "ながねぎ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":5, "freq":4800},
        "ウェルカモ":{"id":913, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["大豆", "ながねぎ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":12, "freq":3600},
        "ウェーニバル":{"id":914, "kind":PK_FIGHTER, "type":"食材", "berry":"クラボ", "ingr":["大豆", "ながねぎ", "オイル"], "main_skill":MS_CHARGE_STRENGTH_M, "fp":20, "freq":2600},
        "ホゲータ":{"id":909, "kind":PK_FIRE, "type":"食材", "berry":"ヒメリ", "ingr":["リンゴ", "ミート", "ハーブ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":4200},
        "アチゲータ":{"id":910, "kind":PK_FIRE, "type":"食材", "berry":"ヒメリ", "ingr":["リンゴ", "ミート", "ハーブ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3100},
        "ラウドボーン":{"id":911, "kind":PK_GHOST, "type":"食材", "berry":"ブリー", "ingr":["リンゴ", "ミート", "ハーブ"], "main_skill":MS_ENERGY_CHARGE_S, "fp":20, "freq":2700},
        "ニャオハ":{"id":906, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["ポテト", "ミルク", "ジンジャー"], "main_skill":MS_COOKING_POWER_UP_S, "fp":5, "freq":4600},
        "ニャローテ":{"id":907, "kind":PK_GRASS, "type":"食材", "berry":"ドリ", "ingr":["ポテト", "ミルク", "ジンジャー"], "main_skill":MS_COOKING_POWER_UP_S, "fp":12, "freq":3500},
        "マスカーニャ":{"id":908, "kind":PK_AKU, "type":"食材", "berry":"ウイ", "ingr":["ポテト", "ミルク", "ジンジャー"], "main_skill":MS_COOKING_POWER_UP_S, "fp":20, "freq":2600},
        "ウパー":{"id":194, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["キノコ", "ポテト", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":5900},
        "ヌオー":{"id":195, "kind":PK_WATER, "type":"食材", "berry":"オレン", "ingr":["キノコ", "ポテト", "ミート"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3400},
        "ウパー(パルデア)":{"id":194, "kind":PK_POISON, "type":"食材", "berry":"カゴ", "ingr":["カカオ", "コーヒー", "ポテト"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":6400},
        "ドオー":{"id":980, "kind":PK_POISON, "type":"食材", "berry":"カゴ", "ingr":["カカオ", "コーヒー", "ポテト"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":3500},
        "ココドラ":{"id":304, "kind":PK_METAL, "type":"食材", "berry":"ベリブ", "ingr":["ミート", "コーヒー", "大豆"], "main_skill":MS_ENERGY_CHARGE_S, "fp":5, "freq":5700},
        "コドラ":{"id":305, "kind":PK_METAL, "type":"食材", "berry":"ベリブ", "ingr":["ミート", "コーヒー", "大豆"], "main_skill":MS_ENERGY_CHARGE_S, "fp":12, "freq":4200},
        "ボスゴドラ":{"id":306, "kind":PK_METAL, "type":"食材", "berry":"ベリブ", "ingr":["ミート", "コーヒー", "大豆"], "main_skill":MS_ENERGY_CHARGE_S, "fp":20, "freq":3000},
        "コリンク":{"id":403, "kind":PK_ELECTRIC, "type":"食材", "berry":"ウブ", "ingr":["トマト", "オイル", "コーヒー"], "main_skill": MS_COOKING_POWER_UP_S, "fp":5, "freq":4400},
        "ルクシオ":{"id":404, "kind":PK_ELECTRIC, "type":"食材", "berry":"ウブ", "ingr":["トマト", "オイル", "コーヒー"], "main_skill": MS_COOKING_POWER_UP_S, "fp":12, "freq":3200},
        "レントラー":{"id":405, "kind":PK_ELECTRIC, "type":"食材", "berry":"ウブ", "ingr":["トマト", "オイル", "コーヒー"], "main_skill": MS_COOKING_POWER_UP_S, "fp":20, "freq":2400},
        "アゴジムシ":{"id":736, "kind":PK_INSECT, "type":"食材", "berry":"ラム", "ingr":["コーヒー", "キノコ", "ミツ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":5, "freq":4600},
        "デンヂムシ":{"id":737, "kind":PK_INSECT, "type":"食材", "berry":"ラム", "ingr":["コーヒー", "キノコ", "ミツ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":12, "freq":3300},
        "クワガノン":{"id":738, "kind":PK_INSECT, "type":"食材", "berry":"ラム", "ingr":["コーヒー", "キノコ", "ミツ"], "main_skill":MS_CHARGE_STRENGTH_S, "fp":20, "freq":2800},
        "ミミッキュ":{"id":778, "kind":PK_GHOST, "type":"スキル", "berry":"ブリー", "ingr":["リンゴ", "コーヒー", "キノコ"], "main_skill":MS_BERRY_BURST, "fp":16, "freq":2500},
        "ニューラ":{"id":215, "kind":PK_AKU, "type":"きのみ", "berry":"ウイ", "ingr":["ミート", "エッグ", "大豆"], "main_skill":MS_TASTY_CHANCE, "fp":16, "freq":3200},
        "マニューラ":{"id":461, "kind":PK_AKU, "type":"きのみ", "berry":"ウイ", "ingr":["ミート", "エッグ", "大豆"], "main_skill":MS_TASTY_CHANCE, "fp":20, "freq":2700},
        "ロコン(アローラ)":{"id":37, "kind":PK_ICE, "type":"きのみ", "berry":"チーゴ", "ingr":["大豆", "コーン", "ポテト"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":5, "freq":5600},
        "キュウコン(アローラ)":{"id":38, "kind":PK_ICE, "type":"きのみ", "berry":"チーゴ", "ingr":["大豆", "コーン", "ポテト"], "main_skill":MS_EXTRA_HELPFUL_S, "fp":20, "freq":2900},
        "ワシボン":{"id":627, "kind":PK_FLY, "type":"スキル", "berry":"シーヤ", "ingr":["ミート", "コーン", "コーヒー"], "main_skill":MS_BERRY_BURST, "fp":5, "freq":3800},
        "ヴォーグル":{"id":628, "kind":PK_FLY, "type":"スキル", "berry":"シーヤ", "ingr":["ミート", "コーン", "コーヒー"], "main_skill":MS_BERRY_BURST, "fp":12, "freq":2400},
        "パモ":{"id":921, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["カカオ", "ミルク", "エッグ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":5, "freq":4600},
        "パモット":{"id":922, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["カカオ", "ミルク", "エッグ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":12, "freq":3300},
        "パーモット":{"id":923, "kind":PK_ELECTRIC, "type":"スキル", "berry":"ウブ", "ingr":["カカオ", "ミルク", "エッグ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":22, "freq":2400},
        "クレセリア":{"id":488, "kind":PK_ESP, "type":"スキル", "berry":"マゴ", "ingr":["ジンジャー", "カカオ", "トマト"], "main_skill":MS_LUNAR_BRESSING, "fp":30, "freq":2300},
        "ダークライ":{"id":491, "kind":PK_AKU, "type":"オール", "berry":"ウイ", "ingr":["ミート", "ミート", "ミート"], "main_skill":MS_NIGHTMARE, "fp":30, "freq":2900},
        "ピンプク":{"id":440, "kind":PK_NORMAL, "type":"食材", "berry":"キー", "ingr":["エッグ", "ポテト", "ミツ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":5, "freq":4500},
        "ラッキー":{"id":113, "kind":PK_NORMAL, "type":"食材", "berry":"キー", "ingr":["エッグ", "ポテト", "ミツ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":16, "freq":3300},
        "ハピナス":{"id":242, "kind":PK_NORMAL, "type":"食材", "berry":"キー", "ingr":["エッグ", "ポテト", "ミツ"], "main_skill":MS_ENERGY_4_EVERYONE, "fp":20, "freq":3100},
}

PROBABILITY = {"フシギダネ": {"ingr":25.70, "skill":1.90},
                "フシギソウ": {"ingr":25.50, "skill":1.90},
                "フシギバナ": {"ingr":26.60, "skill":2.10},
                "ヒトカゲ": {"ingr":20.10, "skill":1.10},
                "リザード": {"ingr":22.70, "skill":1.60},
                "リザードン": {"ingr":22.40, "skill":1.60},
                "ゼニガメ": {"ingr":27.10, "skill":2.00},
                "カメール": {"ingr":27.10, "skill":2.00},
                "カメックス": {"ingr":27.50, "skill":2.10},
                "キャタピー": {"ingr":17.90, "skill":0.80},
                "トランセル": {"ingr":20.80, "skill":1.80},
                "バタフリー": {"ingr":19.70, "skill":1.40},
                "コラッタ": {"ingr":23.70, "skill":3.00},
                "ラッタ": {"ingr":23.70, "skill":3.00},
                "アーボ": {"ingr":23.50, "skill":3.30},
                "アーボック": {"ingr":26.40, "skill":5.70},
                "ピカチュウ": {"ingr":20.70, "skill":2.10},
                "ピカチュウハロウィン": {"ingr":21.80, "skill":2.80},
                "ピカチュウホリデー": {"ingr":13.10, "skill":4.20},
                "ライチュウ": {"ingr":22.40, "skill":3.20},
                "ピッピ": {"ingr":16.80, "skill":3.60},
                "ピクシー": {"ingr":16.80, "skill":3.60},
                "ロコン": {"ingr":16.80, "skill":2.70},
                "キュウコン": {"ingr":16.40, "skill":2.50},
                "プリン": {"ingr":18.20, "skill":4.30},
                "プクリン": {"ingr":17.40, "skill":4.00},
                "ディグダ": {"ingr":19.20, "skill":2.10},
                "ダグトリオ": {"ingr":19.00, "skill":2.00},
                "ニャース": {"ingr":16.30, "skill":4.20},
                "ペルシアン": {"ingr":16.90, "skill":4.40},
                "コダック": {"ingr":13.60, "skill":12.60},
                "ゴルダック": {"ingr":16.20, "skill":12.50},
                "マンキー": {"ingr":19.70, "skill":2.20},
                "オコリザル": {"ingr":20.00, "skill":2.40},
                "ガーディ": {"ingr":13.80, "skill":5.00},
                "ウインディ": {"ingr":13.60, "skill":4.90},
                "マダツボミ": {"ingr":23.30, "skill":3.90},
                "ウツドン": {"ingr":23.50, "skill":4.00},
                "ウツボット": {"ingr":23.30, "skill":3.90},
                "イシツブテ": {"ingr":28.10, "skill":5.20},
                "ゴローン": {"ingr":27.20, "skill":4.80},
                "ゴローニャ": {"ingr":28.00, "skill":5.20},
                "ヤドン": {"ingr":15.10, "skill":6.70},
                "ヤドラン": {"ingr":19.70, "skill":6.80},
                "コイル": {"ingr":18.20, "skill":6.40},
                "レアコイル": {"ingr":18.20, "skill":6.30},
                "ドードー": {"ingr":18.40, "skill":2.00},
                "ドードリオ": {"ingr":18.40, "skill":2.00},
                "ゴース": {"ingr":14.40, "skill":1.50},
                "ゴースト": {"ingr":15.70, "skill":2.20},
                "ゲンガー": {"ingr":16.10, "skill":2.40},
                "イワーク": {"ingr":13.20, "skill":2.30},
                "カラカラ": {"ingr":22.30, "skill":4.40},
                "ガラガラ": {"ingr":22.50, "skill":4.50},
                "ガルーラ": {"ingr":22.20, "skill":1.70},
                "バリヤード": {"ingr":21.60, "skill":3.90},
                "カイロス": {"ingr":21.60, "skill":3.10},
                "メタモン": {"ingr":20.10, "skill":3.60},
                "イーブイ": {"ingr":19.20, "skill":5.50},
                "シャワーズ": {"ingr":21.20, "skill":6.10},
                "サンダース": {"ingr":15.10, "skill":3.90},
                "ブースター": {"ingr":18.50, "skill":5.20},
                "ミニリュウ": {"ingr":25.00, "skill":2.00},
                "ハクリュー": {"ingr":26.20, "skill":2.50},
                "カイリュー": {"ingr":26.40, "skill":2.60},
                "チコリータ": {"ingr":16.90, "skill":3.90},
                "ベイリーフ": {"ingr":16.80, "skill":3.80},
                "メガニウム": {"ingr":17.50, "skill":4.60},
                "ヒノアラシ": {"ingr":18.60, "skill":2.10},
                "マグマラシ": {"ingr":21.10, "skill":4.10},
                "バクフーン": {"ingr":20.80, "skill":3.90},
                "ワニノコ": {"ingr":25.30, "skill":5.20},
                "アリゲイツ": {"ingr":25.30, "skill":5.20},
                "オーダイル": {"ingr":25.70, "skill":5.50},
                "ピチュー": {"ingr":21.00, "skill":2.30},
                "ピィ": {"ingr":16.40, "skill":3.40},
                "ププリン": {"ingr":17.00, "skill":3.80},
                "トゲピー": {"ingr":15.10, "skill":4.90},
                "トゲチック": {"ingr":16.30, "skill":5.60},
                "メリープ": {"ingr":12.80, "skill":4.70},
                "モココ": {"ingr":12.70, "skill":4.60},
                "デンリュウ": {"ingr":13.00, "skill":4.70},
                "ウソッキー": {"ingr":21.70, "skill":7.20},
                "エーフィ": {"ingr":16.40, "skill":4.40},
                "ブラッキー": {"ingr":21.90, "skill":10.10},
                "ヤドキング": {"ingr":16.60, "skill":7.40},
                "ソーナンス": {"ingr":21.10, "skill":6.40},
                "ハガネール": {"ingr":15.40, "skill":3.20},
                "ヘラクロス": {"ingr":15.80, "skill":4.70},
                "デリバード": {"ingr":18.80, "skill":1.50},
                "デルビル": {"ingr":20.10, "skill":4.40},
                "ヘルガー": {"ingr":20.30, "skill":4.60},
                "ライコウ": {"ingr":19.20, "skill":1.90},
                # "ライコウ": {"ingr":19.20, "skill":100},
                "エンテイ": {"ingr":18.70, "skill":2.30},
                "スイクン": {"ingr":27.0, "skill":2.60},
                "ヨーギラス": {"ingr":23.80, "skill":4.10},
                "サナギラス": {"ingr":24.70, "skill":4.50},
                "バンギラス": {"ingr":26.60, "skill":5.20},
                "ラルトス": {"ingr":14.50, "skill":4.30},
                "キルリア": {"ingr":14.60, "skill":4.30},
                "サーナイト": {"ingr":14.40, "skill":4.20},
                "ナマケロ": {"ingr":21.60, "skill":1.90},
                "ヤルキモノ": {"ingr":20.40, "skill":1.50},
                "ケッキング": {"ingr":33.90, "skill":6.70},
                "ヤミラミ": {"ingr":18.80, "skill":6.80},
                "ゴクリン": {"ingr":21.40, "skill":6.30},
                "マルノーム": {"ingr":21.00, "skill":7.00},
                "チルット": {"ingr":17.70, "skill":3.20},
                "チルタリス": {"ingr":25.80, "skill":6.10},
                "カゲボウズ": {"ingr":17.10, "skill":2.60},
                "ジュペッタ": {"ingr":17.90, "skill":3.30},
                "アブソル": {"ingr":17.80, "skill":3.80},
                "ソーナノ": {"ingr":21.30, "skill":5.90},
                "タマザラシ": {"ingr":22.40, "skill":2.30},
                "トドグラー": {"ingr":22.10, "skill":2.10},
                "トドゼルガ": {"ingr":22.30, "skill":2.20},
                "ウソハチ": {"ingr":18.90, "skill":6.10},
                "マネネ": {"ingr":20.10, "skill":3.20},
                "リオル": {"ingr":12.60, "skill":3.80},
                "ルカリオ": {"ingr":15.00, "skill":5.10},
                "グレッグル": {"ingr":22.80, "skill":4.20},
                "ドクロッグ": {"ingr":22.90, "skill":4.30},
                "ユキカブリ": {"ingr":25.10, "skill":4.40},
                "ユキノオー": {"ingr":25.00, "skill":4.40},
                "ジバコイル": {"ingr":17.90, "skill":6.20},
                "トゲキッス": {"ingr":15.80, "skill":5.30},
                "リーフィア": {"ingr":20.50, "skill":5.90},
                "グレイシア": {"ingr":21.90, "skill":6.30},
                "エルレイド": {"ingr":14.70, "skill":5.40},
                "ムンナ": {"ingr":19.70, "skill":4.30},
                "ムシャーナ": {"ingr":18.80, "skill":4.10},
                "ニンフィア": {"ingr":17.80, "skill":4.00},
                "デデンネ": {"ingr":17.70, "skill":4.50},
                "ヌイコグマ": {"ingr":22.50, "skill":1.10},
                "キテルグマ": {"ingr":22.90, "skill":1.30},
                "キュワワー": {"ingr":16.70, "skill":3.0},
                "ウッウ": {"ingr":16.50, "skill":3.90},
                "クワッス": {"ingr":26.1, "skill":2.8},
                "ウェルカモ": {"ingr":25.9, "skill":2.7},
                "ウェーニバル": {"ingr":23.2, "skill":2.4},
                "ホゲータ": {"ingr":25.4, "skill":5.3},
                "アチゲータ": {"ingr":24.7, "skill":5.0},
                "ラウドボーン": {"ingr":26.8, "skill":6.2},
                "ニャオハ": {"ingr":20.8, "skill":2.3},
                "ニャローテ": {"ingr":20.9, "skill":2.3},
                "マスカーニャ": {"ingr":19.0, "skill":2.3},
                "ウパー": {"ingr":20.1, "skill":3.8}, # 暫定値
                "ヌオー": {"ingr":19.0, "skill":3.2}, # 暫定値
                "ウパー(パルデア)": {"ingr":20.9, "skill":5.6}, # 暫定値
                "ドオー": {"ingr":20.8, "skill":5.5}, # 暫定値
                "ココドラ": {"ingr":27.3, "skill":4.6},
                "コドラ": {"ingr":27.7, "skill":4.8},
                "ボスゴドラ": {"ingr":28.5, "skill":5.2}, # 暫定
                "コリンク": {"ingr":18.1, "skill":1.8},
                "ルクシオ": {"ingr":18.2, "skill":1.8},
                "レントラー": {"ingr":20.0, "skill":2.3}, # 暫定
                "アゴジムシ": {"ingr":15.5, "skill":2.9},
                "デンヂムシ": {"ingr":15.4, "skill":2.8},
                "クワガノン": {"ingr":19.4, "skill":5.1},
                "ミミッキュ": {"ingr":15.3, "skill":3.3},
                "ニューラ": {"ingr":25.5, "skill":1.9},
                "マニューラ": {"ingr":25.1, "skill":1.8},
                "ロコン(アローラ)": {"ingr":23.0, "skill":2.8},
                "キュウコン(アローラ)": {"ingr":23.2, "skill":2.8},
                "ワシボン": {"ingr":12.5, "skill":3.1},
                "ヴォーグル": {"ingr":12.1, "skill":3.2},
                "パモ": {"ingr":11.1, "skill":3.6},
                "パモット": {"ingr":10.9, "skill":3.6},
                "パーモット": {"ingr":14.1, "skill":3.9},
                "クレセリア": {"ingr":23.9, "skill":4.1},
                "ダークライ": {"ingr":19.2, "skill":2.3},
                "ピンプク": {"ingr":23.6, "skill":2.3},
                "ラッキー": {"ingr":23.8, "skill":2.3},
                "ハピナス": {"ingr":21.0, "skill":1.3},
    }

INVENTORY = {
    "フシギダネ": 11,
    "フシギソウ": 14,
    "フシギバナ": 17,
    "ヒトカゲ": 12,
    "リザード": 15,
    "リザードン": 19,
    "ゼニガメ": 10,
    "カメール": 14,
    "カメックス": 17,
    "キャタピー": 11,
    "トランセル": 13,
    "バタフリー": 21,
    "コラッタ": 10,
    "ラッタ": 16,
    "アーボ": 10,
    "アーボック": 14,
    "ピカチュウ": 17,
    "ピカチュウハロウィン": 18,
    "ピカチュウホリデー": 16,
    "ライチュウ": 21,
    "ピッピ": 16,
    "ピクシー": 24,
    "ロコン": 13,
    "キュウコン": 23,
    "プリン": 9,
    "プクリン": 13,
    "ディグダ": 10,
    "ダグトリオ": 16,
    "ニャース": 9,
    "ペルシアン": 12,
    "コダック": 8,
    "ゴルダック": 11,
    "マンキー": 12,
    "オコリザル": 17,
    "ガーディ": 8,
    "ウインディ": 16,
    "マダツボミ": 8,
    "ウツドン": 12,
    "ウツボット": 17,
    "イシツブテ": 9,
    "ゴローン": 12,
    "ゴローニャ": 16,
    "ヤドン": 9,
    "ヤドラン": 16,
    "コイル": 8,
    "レアコイル": 11,
    "ドードー": 13,
    "ドードリオ": 21,
    "ゴース": 10,
    "ゴースト": 14,
    "ゲンガー": 18,
    "イワーク": 22,
    "カラカラ": 10,
    "ガラガラ": 15,
    "ガルーラ": 21,
    "バリヤード": 17,
    "カイロス": 24,
    "メタモン": 17,
    "イーブイ": 12,
    "シャワーズ": 13,
    "サンダース": 17,
    "ブースター": 14,
    "ミニリュウ": 9,
    "ハクリュー": 12,
    "カイリュー": 20,
    "チコリータ": 12,
    "ベイリーフ": 17,
    "メガニウム": 20,
    "ヒノアラシ": 14,
    "マグマラシ": 18,
    "バクフーン": 23,
    "ワニノコ": 11,
    "アリゲイツ": 15,
    "オーダイル": 19,
    "ピチュー": 10,
    "ピィ": 10,
    "ププリン": 8,
    "トゲピー": 8,
    "トゲチック": 10,
    "メリープ": 9,
    "モココ": 11,
    "デンリュウ": 15,
    "ウソッキー": 16,
    "エーフィ": 16,
    "ブラッキー": 14,
    "ヤドキング": 17,
    "ソーナンス": 10,
    "ハガネール": 25,
    "ヘラクロス": 20,
    "デリバード": 20,
    "デルビル": 10,
    "ヘルガー": 18,
    "ライコウ": 22,
    "エンテイ": 19,
    "スイクン": 17,
    "ヨーギラス": 9,
    "サナギラス": 13,
    "バンギラス": 19,
    "ラルトス": 9,
    "キルリア": 13,
    "サーナイト": 18,
    "ナマケロ": 7,
    "ヤルキモノ": 9,
    "ケッキング": 12,
    "ヤミラミ": 16,
    "ゴクリン": 8,
    "マルノーム": 19,
    "チルット": 12,
    "チルタリス": 14,
    "カゲボウズ": 11,
    "ジュペッタ": 19,
    "アブソル": 21,
    "ソーナノ": 7,
    "タマザラシ": 9,
    "トドグラー": 13,
    "トドゼルガ": 18,
    "ウソハチ": 8,
    "マネネ": 10,
    "リオル": 9,
    "ルカリオ": 14,
    "グレッグル": 10,
    "ドクロッグ": 14,
    "ユキカブリ": 10,
    "ユキノオー": 21,
    "ジバコイル": 13,
    "トゲキッス": 16,
    "リーフィア": 13,
    "グレイシア": 12,
    "エルレイド": 19,
    "ムンナ": 12,
    "ムシャーナ": 23,
    "ニンフィア": 15,
    "デデンネ": 19,
    "ヌイコグマ": 13,
    "キテルグマ": 20,
    "キュワワー": 20,
    "ウッウ": 19,
    "クワッス":10,
    "ウェルカモ":14,
    "ウェーニバル":19,
    "ホゲータ":11,
    "アチゲータ":16,
    "ラウドボーン":19,
    "ニャオハ":10,
    "ニャローテ":14,
    "マスカーニャ":18,
    "ウパー":10,
    "ヌオー":16,
    "ウパー(パルデア)":9,
    "ドオー":20,
    "ココドラ":10,
    "コドラ":13,
    "ボスゴドラ":18,
    "コリンク":11,
    "ルクシオ":16,
    "レントラー":21,
    "アゴジムシ":11,
    "デンヂムシ":15,
    "クワガノン":19,
    "ミミッキュ":19,
    "ニューラ":17,
    "マニューラ":21,
    "ロコン(アローラ)":10,
    "キュウコン(アローラ)":20,
    "ワシボン":10,
    "ヴォーグル":18,
    "パモ":9,
    "パモット":12,
    "パーモット":18,
    "クレセリア":22,
    "ダークライ":28,
    "ピンプク": 7,
    "ラッキー": 15,
    "ハピナス": 21,
}

ID_RECIPE_CURRY = 0
ID_RECIPE_SALAD = 1
ID_RECIPE_DEZERT = 2
RECIPE = {
    ID_RECIPE_SALAD:[
                {"lv":63, "name":"まけんきコーヒーサラダ", "description":"負けん気で何度も挑戦しついに完成したコーヒーソースのサラダ。", "ingredients":["コーヒー", "ミート", "オイル", "ポテト"], "amounts":[28, 28, 22, 22], "n":100, "base_energy":20218},
                {"lv":59, "name":"ワカクササラダ", "description":"ワカクサの島でとれた新鮮野菜だけをつかったサラダ。", "ingredients": ["オイル", "コーン","トマト","ポテト"], "amounts": [22,17,14,9], "n": 62, "base_energy": 11393, },
                {"lv":54, "name":"ニンジャサラダ", "description":"とうふを使ったニンジャ好みの味付けで、素早く食べられる。", "ingredients": ["ジンジャー", "大豆", "キノコ","ながねぎ"], "amounts": [11, 19, 12, 15], "n": 57, "base_energy": 11659, },
                {"lv":46, "name":"めいそうスイートサラダ", "description":"さわやかな甘みがこころを落ち着かせる。", "ingredients": ["リンゴ", "ミツ", "コーン"], "amounts": [21, 16, 12], "n": 49, "base_energy": 7675, },
                {"lv":15, "name":"クロスチョップドサラダ", "description":"チョップを重ねて細かくつくったチョップドサラダ。", "ingredients":["エッグ", "ミート", "コーン", "トマト"], "amounts":[20, 15, 11, 10], "n":56, "base_energy":8755},
                {"lv":8, "name":"ヤドンテールのペッパーサラダ", "description":"ピリッと辛いスパイスがテールのあまみをより際立たせる。", "ingredients": ["ハーブ", "オイル", "シッポ"], "amounts": [10, 15, 10], "n": 35, "base_energy": 8169, },
                {"lv":12, "name":"キノコのほうしサラダ", "description":"睡眠に良い成分がふんだんに入ったサラダ。", "ingredients": ["キノコ", "オイル", "トマト"], "amounts": [17, 8, 8], "n": 33, "base_energy": 5859, },
                {"lv":45, "name":"オーバーヒートサラダ", "description":"特製のしょうがドレッシングがからだを熱くさせる。", "ingredients": ["ハーブ", "ジンジャー", "トマト"], "amounts": [17, 10, 8], "n": 35, "base_energy": 5225, },
                {"lv":13, "name":"くいしんぼうポテトサラダ", "description":"とくせんリンゴが隠し味のポテトサラダ。", "ingredients": ["ポテト", "エッグ", "ミート", "リンゴ"], "amounts": [14, 9, 7, 6], "n": 36, "base_energy": 5040, },
                {"lv":35, "name":"ムラっけチョコミートサラダ", "description":"しょっぱいソースとあまいチョコソースの味の変化が楽しめる。", "ingredients": ["カカオ", "ミート"], "amounts": [14, 9], "n": 23, "base_energy": 3558, },
                {"lv":9, "name":"ばかぢからワイルドサラダ", "description":"これ1つで1日分の栄養がとれるボリュームサラダ。", "ingredients": ["ミート", "ジンジャー", "エッグ", "ポテト"], "amounts": [9, 6, 5, 3], "n": 23, "base_energy": 2958, },
                {"lv":8, "name":"モーモーカプレーゼ", "description":"チーズとトマトにオイルをかけただけのシンプルサラダ。", "ingredients": ["ミルク", "トマト", "オイル"], "amounts": [12, 6, 5], "n": 23, "base_energy": 2856, },
                {"lv":1, "name":"みだれづきコーンサラダ", "description":"山盛りのコーンを突いて食べるサラダ。", "ingredients": ["コーン", "オイル"], "amounts": [9, 8], "n": 17, "base_energy": 2785, },
                {"lv":1, "name":"めんえきねぎサラダ", "description":"シャキっと食感のねぎでめんえき力が上がるサラダ。", "ingredients": ["ジンジャー", "ながねぎ"], "amounts": [5, 10], "n": 15, "base_energy": 2658, },
                {"lv":12, "name":"メロメロりんごのチーズサラダ", "description":"相性ばつぐんの食材を活かすため、味付けはシンプルに。", "ingredients": ["リンゴ", "ミルク", "オイル"], "amounts": [15, 5, 3], "n": 23, "base_energy": 2578, },
                {"lv":14, "name":"ねっぷうとうふサラダ", "description":"真っ赤な辛いソースのとうふサラダ。", "ingredients": ["ハーブ", "大豆"], "amounts": [6, 10], "n": 16, "base_energy": 1976, },
                {"lv":30, "name":"ゆきかきシーザーサラダ", "description":"雪のようにふりかけたチーズをかきわけて食べるベーコンサラダ。", "ingredients": ["ミルク", "ミート"], "amounts": [10, 6], "n": 16, "base_energy": 1774, },
                {"lv":1, "name":"うるおいとうふサラダ", "description":"ぷるっとしたとうふがのったサラダ。", "ingredients": ["大豆", "トマト"], "amounts": [15, 6], "n": 21, "base_energy": 3113, },
                {"lv":5, "name":"あんみんトマトサラダ", "description":"あんみんトマトの成分でねむりを助けるシンプルサラダ。", "ingredients": ["トマト"], "amounts": [8], "n": 8, "base_energy": 933, },
                {"lv":7, "name":"マメハムサラダ", "description":"マメミートでつくったハムのシンプルサラダ。", "ingredients": ["ミート"], "amounts": [8], "n": 8, "base_energy": 873, },
                {"lv":23, "name":"とくせんリンゴサラダ", "description":"リンゴをすりつぶして作ったドレッシングのシンプルサラダ。", "ingredients": ["リンゴ"], "amounts": [8], "n": 8, "base_energy": 763, },
    ],
    ID_RECIPE_CURRY:[
                {"lv":65, "name":"めざめるパワーシチュー", "description":"目覚めを豪華に彩る具だくさんのトマトシチュー。", "ingredients":["大豆", "トマト", "キノコ", "コーヒー"], "amounts":[28, 25, 23, 16], "n":92, "base_energy":19061},
                {"lv":46, "name":"れんごくコーンキーマカレー", "description":"コーンの甘みの後にはれんごくのような辛さがやってくる。", "ingredients":["ハーブ","ミート", "コーン","ジンジャー"], "amounts":[27,24,14,12], "n":77, "base_energy": 13690,},
                {"lv":57, "name":"ニンジャカレー", "description":"ニンジャが好んで食べたと言い伝えられているとうふのカレー。", "ingredients":["大豆", "ながねぎ", "ミート", "キノコ"], "amounts":[24,12,9,5], "n":50, "base_energy": 9445,},
                {"lv":55, "name":"ぜったいねむりバターカレー", "description":"深いねむりをテーマに食材を選んだカレー。", "ingredients":["ポテト", "カカオ", "トマト", "ミルク"], "amounts":[18,12,15,10], "n":55, "base_energy": 9010,},
                {"lv":17, "name":"あぶりテールカレー", "description":"テールのうまみがルーをワンランク上の味に。", "ingredients":["シッポ", "ハーブ", ], "amounts":[8 ,25,], "n":33, "base_energy": 7483,},
                {"lv":20, "name":"からくちネギもりカレー", "description":"香ばしく焼いたネギは果実のように甘く、ルーの辛さと絶妙のバランス。", "ingredients":["ながねぎ", "ジンジャー", "ハーブ"], "amounts":[14,10,8], "n":32, "base_energy": 5900,},
                {"lv":24, "name":"ピヨピヨパンチ辛口カレー", "description":"リズミカルに甘みと辛みが広がり最後に苦みが訪れる。", "ingredients":["コーヒー", "ハーブ", "ミツ"], "amounts":[11, 11, 11], "n":33, "base_energy":5702},
                {"lv":16, "name":"じゅうなんコーンシチュー", "description":"ミルクとコーンのやわらかい甘みがやさしいホワイトシチュー。", "ingredients":["コーン", "ミルク", "ポテト"], "amounts":[14,8,8], "n":30, "base_energy": 4670,},
                {"lv":13, "name":"おやこあいカレー", "description":"子供にやさしい食材だけでつくった愛情たっぷりカレー。", "ingredients":["ミツ", "エッグ", "リンゴ", "ポテト"], "amounts":[12,8,11,4], "n":35, "base_energy": 4523,},
                {"lv":6, "name":"キノコのほうしカレー", "description":"キノコのほうしを浴びたかのように眠れるカレー。", "ingredients":["キノコ", "ポテト", ], "amounts":[14,9,], "n":23, "base_energy": 4041,},
                {"lv":30, "name":"ビルドアップマメカレー", "description":"身体づくりに必要な栄養をたっぷりつめこんだボリュームカレー。", "ingredients":["大豆","ミート", "エッグ", "ハーブ"], "amounts":[12,6, 4, 4], "n":26, "base_energy": 3274,},
                {"lv":52, "name":"満腹チーズバーグカレー", "description":"ボリュームたっぷり。カビゴンもびっくり大きなカレー。", "ingredients":["ミルク", "ミート"], "amounts":[8 ,8], "n":16, "base_energy": 1785,},
                {"lv":1, "name":"ほっこりホワイトシチュー", "description":"とけてなくなる寸前までポテトを煮込んだトロトロシチュー。", "ingredients":["ミルク", "ポテト", "キノコ"], "amounts":[10,8,4], "n":22, "base_energy": 3089,},
                {"lv":1, "name":"とけるオムカレー", "description":"絶妙な火入れで仕上げたオムレツが舌の上でとけるカレー。", "ingredients":["エッグ","トマト"], "amounts":[10,6], "n":16, "base_energy": 2009,},
                {"lv":1, "name":"サンパワートマトカレー", "description":"太陽の光で真っ赤に育ったトマトでつくったカレー。", "ingredients":["トマト", "ハーブ", ], "amounts":[10,5,], "n":15, "base_energy": 1943,},
                {"lv":7, "name":"ひでりカツレツカレー", "description":"揚げたてのカツがキラッと光る。", "ingredients":["ミート", "オイル"], "amounts":[10,5], "n":15, "base_energy": 1815,},
                {"lv":7, "name":"マメバーグカレー", "description":"マメでつくったやわらかハンバーグが主役。", "ingredients":["ミート"], "amounts":[7 ,], "n":7, "base_energy": 764,},
                {"lv":10, "name":"ベイビィハニーカレー", "description":"子供でも食べられる、ミツたっぷりの甘口カレー。", "ingredients":["ミツ"], "amounts":[7 ,], "n":7, "base_energy": 749,},
                {"lv":3, "name":"たんじゅんホワイトシチュー", "description":"ミルクのうまみを感じるシンプルシチュー。", "ingredients":["ミルク"], "amounts":[7 ,], "n":7, "base_energy": 727,},
                {"lv":8, "name":"とくせんリンゴカレー", "description":"りんごの自然な甘みを感じるシンプルなカレー。", "ingredients":["リンゴ"], "amounts":[7 ,], "n":7, "base_energy": 668,},
        ],
    ID_RECIPE_DEZERT:[
                {"lv":54, "name":"ドオーのエクレア", "description":"", "ingredients":["カカオ", "ミルク", "コーヒー", "ミツ"], "amounts":[30, 26, 24, 22], "n":102, "base_energy":20885},
                {"lv":56, "name":"スパークスパイスコーラ", "description":"スカッと目が覚める刺激の強いコーラ。", "ingredients":["リンゴ", "ジンジャー", "ながねぎ", "コーヒー"], "amounts":[35, 20, 20, 12], "n":87, "base_energy":17494},
                {"lv":53, "name": "おちゃかいコーンスコーン", "description": "サクサク食感のスコーンとアップルジンジャーのジャムを1対1で。", "ingredients":["リンゴ", "ジンジャー", "コーン","ミルク"], "amounts":[20, 20, 18, 9], "n":67, "base_energy": 10925, },
                {"lv":36, "name": "フラワーギフトマカロン", "description": "おくりものにぴったりな笑顔咲くマカロン。", "ingredients":["カカオ", "エッグ", "ミツ", "ミルク"], "amounts":[25, 25, 17, 10], "n":77, "base_energy": 13834, },
                {"lv":45, "name": "かたやぶりコーンティラミス", "description": "", "ingredients":["コーヒー", "コーン", "ミルク"], "amounts":[14, 14, 12], "n":40, "base_energy": 7125, },
                {"lv":50, "name": "ちからもちソイドーナッツ", "description": "サクっとあげたソイドーナッツ。からだづくりのお供に。", "ingredients":["オイル", "カカオ", "大豆"], "amounts":[12,7,16], "n":35, "base_energy": 5547, },
                {"lv":56, "name": "あくまのキッスフルーツオレ", "description": "つかれた体を癒やし、眠りにみちびくリラックスドリンク。", "ingredients":["リンゴ", "ミルク", "ミツ", "カカオ"], "amounts":[11, 9, 7, 8], "n":35, "base_energy": 4734, },
                {"lv":43, "name": "ネロリのデトックスティー", "description": "博士特製のデトックスティー。", "ingredients":["ジンジャー", "リンゴ", "キノコ"], "amounts":[11, 15, 9], "n":35, "base_energy": 5065, },
                {"lv":15, "name": "プリンのプリンアラモード", "description": "ふうせんのような張りをもつ特製プリン。", "ingredients":["ミツ", "エッグ", "リンゴ", "ミルク"], "amounts":[20, 15, 10, 10], "n":55, "base_energy": 7594, },
                {"lv":13, "name":"はやおきコーヒーゼリー", "description":"目覚めを加速させる苦めのコーヒーゼリー。", "ingredients":["コーヒー", "ミルク", "ミツ"], "amounts":[16, 14, 12], "n":42, "base_energy":6793},
                {"lv":25, "name": "だいばくはつポップコーン", "description": "だいばくはつするほどの火力で一瞬で仕上げた。", "ingredients":["コーン", "オイル", "ミルク"], "amounts":[15, 14, 7], "n":36, "base_energy": 6048, },
                {"lv":13, "name": "ふくつのジンジャークッキー", "description": "大変なことがあってもくじけずに頑張るパワーをくれるクッキー。", "ingredients":["ミツ", "ジンジャー", "カカオ", "エッグ"], "amounts":[14, 12, 5, 4], "n":35, "base_energy": 4921, },
                {"lv":36, "name": "はなびらのまいチョコタルト", "description": "食べるとリンゴの花びらが舞うやんちゃなタルト。", "ingredients":["カカオ", "リンゴ"], "amounts":[11, 11], "n":22, "base_energy": 3314, },
                {"lv":17, "name": "あまいかおりチョコケーキ", "description": "あまいかおりには人もポケモンも引き寄せられる。", "ingredients":["ミツ", "カカオ", "ミルク"], "amounts":[9, 8, 7], "n":24, "base_energy": 3280, },
                {"lv":29, "name": "はりきりプロテインスムージー", "description": "トレーニング後のごほうびの甘い一杯。", "ingredients":["大豆", "カカオ"], "amounts":[15, 8], "n":23, "base_energy": 3168, },
                {"lv":20, "name": "おおきいマラサダ", "description": "アローラのレシピを取り寄せ再現した特別なあげパン。", "ingredients":["オイル", "ミルク", "ミツ"], "amounts":[10, 7, 6], "n":23, "base_energy": 2927, },
                {"lv":2, "name": "かるわざソイケーキ", "description": "かるい口当たりに仕上げたソイケーキ。", "ingredients":["エッグ", "大豆"], "amounts":[8, 7], "n":15, "base_energy": 1798, },
                {"lv":7, "name": "マイペースやさいジュース", "description": "自然な甘みと酸味のかんたんなジュース。", "ingredients":["リンゴ", "トマト"], "amounts":[7, 9], "n":16, "base_energy": 1798, },
                {"lv":12, "name": "ひのこのジンジャーティー", "description": "辛いジンジャーにリンゴを合わせることで飲みやすくなった。", "ingredients":["リンゴ", "ジンジャー"], "amounts":[7, 9], "n":16, "base_energy": 1788, },
                {"lv":1, "name": "じゅくせいスイートポテト", "description": "ポテトをうまく熟成させることでミツいらずの甘さに。", "ingredients":["ポテト", "ミルク"], "amounts":[9, 5], "n":14, "base_energy": 1783, },
                {"lv":22, "name": "ねがいごとアップルパイ", "description": "ゴロっとしたリンゴの部分に当たるとラッキー。", "ingredients":["リンゴ", 12, "ミルク"], "amounts":[12, 4], "n":16, "base_energy": 1634, },
                {"lv":13, "name": "クラフトサイコソーダ", "description": "シュワっとはじける手作りソーダ。", "ingredients":["ミツ"], "amounts":[9], "n":9, "base_energy": 964, },
                {"lv":21, "name": "とくせんリンゴジュース", "description": "選びぬかれたリンゴだけでつくった濃厚なジュース。", "ingredients":["リンゴ"], "amounts":[8], "n":8, "base_energy": 763, },
                {"lv":10, "name": "モーモーホットミルク", "description": "温めることで甘みが増したミルク。", "ingredients":["ミルク"], "amounts":[7], "n":7, "base_energy": 727, },
    ],
}


RECIPE_LV_BONUS_TABLE = {
    1:0/100,
    2:2/100,
    3:4/100,
    4:6/100,
    5:8/100,
    6:9/100,
    7:11/100,
    8:13/100,
    9:16/100,
    10:18/100,
    11:19/100,
    12:21/100,
    13:23/100,
    14:24/100,
    15:26/100,
    16:28/100,
    17:30/100,
    18:31/100,
    19:33/100,
    20:35/100,
    21:37/100,
    22:40/100,
    23:42/100,
    24:45/100,
    25:47/100,
    26:50/100,
    27:52/100,
    28:55/100,
    29:58/100,
    30:61/100,
    31:64/100,
    32:67/100,
    33:70/100,
    34:74/100,
    35:77/100,
    36:81/100,
    37:84/100,
    38:88/100,
    39:92/100,
    40:96/100,
    41:100/100,
    42:104/100,
    43:108/100,
    44:113/100,
    45:117/100,
    46:122/100,
    47:127/100,
    48:132/100,
    49:137/100,
    50:142/100,
    51:148/100,
    52:153/100,
    53:159/100,
    54:165/100,
    55:171/100,
    56:177/100,
    57:183/100,
    58:190/100,
    59:197/100,
    60:203/100,
    61:209/100,
    62:215/100,
    63:221/100,
    64:227/100,
    65:234/100,
}
