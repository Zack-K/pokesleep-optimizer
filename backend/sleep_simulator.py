import itertools
from define import * 
import math
import random
import sys
from pokes import *
from scipy.special import comb
from scipy.stats import binom
from scipy.stats import norm
from decimal import Decimal, ROUND_HALF_UP
import copy
from tqdm import tqdm

# batch_test_recipe_consider=[ID_RECIPE_DEZERT, ID_RECIPE_SALAD]
# batch_test_recipe_consider=[ID_RECIPE_DEZERT]
# batch_test_recipe_consider=[ID_RECIPE_CURRY, ID_RECIPE_DEZERT, ID_RECIPE_SALAD]
# batch_test_recipe_consider=[ID_RECIPE_SALAD]
batch_test_recipe_consider=[ID_RECIPE_CURRY]
LOG_LEVEL = 1
BATCH_RUN = True
LOG_LEVEL = 5
BATCH_RUN = False

id_recipe_request=ID_RECIPE_CURRY
# id_recipe_request=ID_RECIPE_SALAD
id_recipe_request=ID_RECIPE_DEZERT

# field_berry=FIELD_BERRY_NONE
# field_berry=FIELD_BERRY_WAKAKUSA
# field_berry=FIELD_BERRY_CYAN
# field_berry=FIELD_BERRY_TAUPE
# field_berry=FIELD_BERRY_SNOWDROP
# field_berry=FIELD_BERRY_LAPIS
field_berry=FIELD_BERRY_OGPP

field_bonus=1.57
pot_capacity=69

supinfo = "_GCT_newyear_1230"
supinfo = "_GCT_newyear_week2_0105"
supinfo = "_GCT_newyear_week2_0106"
supinfo = "_event_0121"
supinfo = "_normal_0203"
supinfo = "_campaign_0210"
supinfo = "_normal_0225"
supinfo = "_Cresselia_week1_GCT"
supinfo = "_Cresselia_week2_GCT"
supinfo = "_Cresselia_week2_GCT_wo_エーフィ"
supinfo = "_Cresselia_week1_GCT_20250331"
supinfo = "_Cresselia_week2_GCT_20250407"
supinfo = "_normal_0417"
supinfo = "_yumekakeget_0420"
supinfo = f"_spring_fes_salad_0505_GCT{GCT}"
supinfo = f"_normal_20250525_GCT{GCT}"
supinfo = f"_dekamori_20250529_GCT{GCT}"
supinfo = f"_normal_20250610_GCT{GCT}"
supinfo = f"_summerfes_20250623_GCT{GCT}"

# 関数one_weekにおける毎週のBAGの初期値
DEFAULT_BAG = {
    # "リンゴ": 100,
    # "ミツ": 0,
    # "ハーブ":0,
    "大豆":50,
    # "ジンジャー":97,
    # "コーン":0,
    # "オイル":300,
    # "ミート":40,
    "トマト":50,
    # "ポテト":270,
    # "カカオ":0,
    # "ミルク":0,
    # "エッグ":0,
    # "ながねぎ":124,
    # "シッポ":98,
    "キノコ":500,
    "コーヒー":350,
}

def main():

    field1 = Field(
        field_bonus=field_bonus,
        field_berry=field_berry,
        pot_capacity=pot_capacity,
        id_recipe_request=id_recipe_request,
    )

    # PARTY = party_from_tab_str("う　さ　ぎ	卵白	ウツボット	ウツボット2	つよイーブイ")
    # PARTY = party_from_tab_str("う　さ　ぎ	卵白	ウツボット	津軽	発電所")
    # PARTY = party_from_tab_str("発電所	つよイーブイ	卵白	ゲンガー	ABAコリンク")
    # PARTY = party_from_tab_str("発電所	卵白	ゲンガー	網目状地響き	きのみピチュー")
    # PARTY = party_from_tab_str("発電所	つよイーブイ	卵白	ありがとう	感激")
    # PARTY = party_from_tab_str("感激	卵白	ウツボット	つよイーブイ	う　さ　ぎ")
    # PARTY = party_from_tab_str("おだやかデデンネ	ウパー	豆の草原	ほりで	バリヤード")
    # PARTY = party_from_tab_str("おだやかデデンネ	キュワワー	ABAコリンク	ウッウ	色違いバリヤード")
    # PARTY = party_from_tab_str("卵白	二毛作	ABAコリンク	おだやかデデンネ	色違いバリヤード")
    PARTY = party_from_tab_str("卵白	朝定食")
    PARTY = party_from_tab_str("お前...	皿田きのこ	もう勘弁	こぴ周作	忙しないよー")
    PARTY = party_from_tab_str("豆の草原	夏やさい	ほりで	ウパー	お前...")
    PARTY = party_from_tab_str("う　さ　ぎ	ゆめぼゼニガメ	山田養蜂場	ほりで	鍋仙人")
    PARTY = party_from_tab_str("つよイーブイ	クレセリア	ありがとう	発電所	忙しないよー")
    PARTY = party_from_tab_str("つよイーブイ	ダークライ	朝定食	迷走たろう	忙しないよー")
    PARTY = party_from_tab_str("発電所	つよイーブイ	ありがとう	感激	忙しないよー")
    PARTY = party_from_tab_str("こぴ周作	つよイーブイ	クレセリア採用	ムシャーナ	忙しないよー")
    PARTY = party_from_tab_str("ゲンガー	食の大陸	もう勘弁	お前...	忙しないよー")
    PARTY = party_from_tab_str("ほりで	お前...	ゆめぼゼニガメ	山田養蜂場	クレセリア採用")
    PARTY = party_from_tab_str("忙しないよー	感激	発電所	お前...	忠犬ライコウ")
    PARTY = party_from_tab_str("つよイーブイ	忠犬ライコウ	感激	忙しないよー	発電所")
    PARTY = party_from_tab_str("スイクン	きのみワニノコ	きのみヤドキング	きのみカメール	卵白")
    # PARTY = party_from_tab_str("つよイーブイ	発電所	ありがとう	感激	卵白")
    # PARTY = party_from_tab_str("発電所	感謝	ありがとう	忙しないよー	ダークライ")
    PARTY = party_from_csv("スイクン,ワニノ唐揚げ,きのみワニノコ,発電所,ウパー")
    PARTY = party_from_csv("忠犬ライコウ,網目状地響き,発電所,ありがとう,たき火")
    PARTY = party_from_csv("スイクン,ワニノ唐揚げ,発電所,ありがとう,きのみワニノコ")
    PARTY = party_from_tab_str("スイクン	きのみワニノコ	きのみヤドキング	きのみカメール	ワニノ唐揚げ")
    PARTY = party_from_tab_str("スイクン	発電所	ほりで	ウパー	忙しないよー")
    PARTY = party_from_tab_str("豆の草原	発電所	夏やさい	感激	忙しないよー")
    PARTY = party_from_tab_str("豆の草原	発電所	夏やさい	お前...	卵白")
    PARTY = party_from_tab_str("豆の草原	発電所	夏やさい	お前...	忙しないよー")
    PARTY = party_from_tab_str("感激	発電所	ウパー	う　さ　ぎ	忙しないよー")
    PARTY = party_from_tab_str("スイクン	発電所	ウパー	う　さ　ぎ	忙しないよー")
    PARTY = party_from_tab_str("スイクン	発電所	ウパー	ワニノ唐揚げ	忙しないよー")

    
    ## field setting at beginning of week
    recipe_name_reserve = "" # この料理の食材はなにがあろうと追加食材として使わない,
    # recipe_name_reserve = "めざめるパワーシチュー" # この料理の食材はなにがあろうと追加食材として使わない,
    # recipe_name_reserve = "まけんきコーヒーサラダ" # この料理の食材はなにがあろうと追加食材として使わない,
    # recipe_name_reserve = "ニンジャカレー" # この料理の食材はなにがあろうと追加食材として使わない,
    monday_setting = {
        "monday_extra_pot_capacity": 0,
        "monday_cooking_successful_rate": 0.1,
        # "monday_extra_pot_capacity": 200,
        # "monday_cooking_successful_rate": 0.7,
    }

    # raise

    n=100
    cumu_e, cumu_ing, cumu_n_ing, cumu_e_rcp = 0, {}, 0, 0
    # dryrun to determine essential ingredients
    _, ing, _, _, _ = one_week(PARTY, field1, cooks=False)
    # omit unstable ingredients
    ing_stable = {}
    for key in ing:
        if ing[key]>35:
            ing_stable[key] = ing[key]
    ing_essential, ing_additional, recipes_primary, n_ing_essential = list_up_possible_recipe(ing_stable, field1, PARTY, recipe_name_reserve=recipe_name_reserve)
    
    # reset counters
    reset_to_Monday(PARTY, field1, **monday_setting)

    # one week test
    for i in range(n):

        # start simulation
        e, ing, bag, rcp, e_rcp = one_week(PARTY, field1, cooks=True, ing_additional=ing_additional, rcp_primary=recipes_primary,
                                           ing_essential=ing_essential, n_ing_essential=n_ing_essential)
        cumu_e += e
        cumu_e_rcp += e_rcp
        for name in ing:
            cumu_n_ing += ing[name]
            if name in cumu_ing:
                cumu_ing[name] += ing[name]
            else:
                cumu_ing[name] = ing[name]
        
        # reset counters
        reset_to_Monday(PARTY, field1, resetsPK=False, **monday_setting)
    
    print2("--- TEST RESULT ---")
    for pk in PARTY:
        pk:Pokemon
        print2(f"* {pk.name}({pk.tribe})")
        print2(f"     エナジー　: {pk.cumulated_energy/7/n:.1f}")
        print2(f"     スキル回数: {pk.n_skill_activated/7/n:.2f}")
        if pk.pokemon['main_skill'] in [MS_EXTRA_HELPFUL_S, MS_HELPER_BOOST]:
            print2(f"  ストック済みエナジー/1week: {pk.extra_help_energy/n:.1f}")
            print2(f"  ストック済み食材/1week: ")
            ing_eng = 0
            for name in pk.extra_help_ingredients:
                print2(f"       {name}: {pk.extra_help_ingredients[name]/n:.2f}")
                ing_eng += pk.extra_help_ingredients[name] * FOOD[name]
            print2(f"       合計エナジー: {ing_eng/n:.1f}")
    print2(f"* レシピエナジー: {cumu_e_rcp/n/7:.1f}")
    print2(f"average energy per day: {cumu_e/n/7:.2f}")
    print2(f"average ing per day: ")
    for name in cumu_ing:
        print2(f"    {name}: {cumu_ing[name]/n/7:.2f}")
    print2(f"avg. recipe energy: {cumu_e_rcp/n/21:.1f}")
    print2(f"recipe priority ({len(recipes_primary)}):")
    for r in recipes_primary:
        print2(f"    {r}", end=", ")
    else:
        print2("")
    
    
    if not BATCH_RUN:
        return
    reset_to_Monday(PARTY, field1, resetsPK=True, **monday_setting)
    
    # various combination
    all = party_from_namelist(
        [
            # "発電所",
            "卵白", 
            "う　さ　ぎ",
            # "すがちゃん", 
            # "ダイナモ", 
            "ありがとう", 
            "ワニノ唐揚げ",
            # "TOUGHグミ", 
            # "調達係長",
            "たけのこ",
            "たき火",
            # "きのみピクシー",
            # "ジュペッタ",
            # "忠犬ライコウ", 
            # "エンテイ", 
            # "スイクン", 
            # "鍋仙人", 
            "つよイーブイ", 
            "感激",
            # "ジバコイル",
            # "網目状地響き", 
            # "シャワーズ",
            # "きのみヤドキング", 
            "忙しないよー", 
            "食の大陸", 
            "ウツボット", 
            "朝定食",
            "津軽",
            "豆の草原",
            "ゲンガー",
            "ウパー",
            "ブラウン農場",
            "二毛作",
            # "キュワワー", 
            "偶然の産物",
            # "ABC食MS",
            "皿田きのこ",
            "肉たろう",
            "夏やさい",
            "ほりで",
            "迷走たろう",
            "もう勘弁", 
            "山田養蜂場", 
            # "カイロス", 
            "こぴ周作",
            "お前...",
            # "きのみフシギダネ",
            "ゆめぼゼニガメ",
            # "きのみワニノコ",
            # "ムシャーナ",
            # "クレセリア採用",
            # "ダークライ",
            # "新鍋仙人", 
            # "筋肉の躍動", 
            # "ドードリオ", 
            # "磐梯山崩壊", 
            # "もういいよ", 
            # "ドブネ二世", 
            # "ワタなんだ", 
            # "今永", 
            # "なめんなよ", 
            # "養蜂家(仮)", 
            # "アブソル",
            # "ヘルガー",
            # "メタモン",
            # "豆担当", 
            # "感謝",
            # "緊急派遣職員",
            # "AABココドラ",
            # "きのみピチュー",
            # "きのみカメール",
            # "きのみ勇敢ピチュー",
        ]
    )

    csv =f"result"
    if field_berry==FIELD_BERRY_WAKAKUSA:
        csv += "_wakakusa"
    elif field_berry==FIELD_BERRY_CYAN:
        csv += "_cyan"
    elif field_berry==FIELD_BERRY_TAUPE:
        csv += "_taupe"
    elif field_berry==FIELD_BERRY_SNOWDROP:
        csv += "_snowdrop"
    elif field_berry==FIELD_BERRY_LAPIS:
        csv += "_lapis"
    elif field_berry==FIELD_BERRY_OGPP:
        csv += "_ogpp"
    csv += f"_pk{FORCE_PK_LV}"
    csv += "_"
    if ID_RECIPE_SALAD in batch_test_recipe_consider:
        csv += "s"
    if ID_RECIPE_DEZERT in batch_test_recipe_consider:
        csv += "d"
    if ID_RECIPE_CURRY in batch_test_recipe_consider:
        csv += "c"
    csv += f"_rcp{FORCE_RECIPE_LV}"
    csv += supinfo
    csv += ".csv"
        
    f = open(csv, "w")
    f.close()
    
    must = []
    # must = party_from_namelist(["二毛作","ウツボット"])
    must = party_from_namelist(["発電所"])
    # must = party_from_namelist(["ありがとう"])
    # must = party_from_namelist(["つよイーブイ", "忙しないよー"])
    # must = party_from_namelist(["肉たろう","ほりで","卵白"])

    
    # start analysis
    for id_r in batch_test_recipe_consider:
        field1 = Field(
            field_bonus=field_bonus,
            field_berry=field_berry,
            pot_capacity=pot_capacity,
            id_recipe_request=id_r,
        )
        # dry run
        # combination_bf(must, all, 1, field1, outfp=csv)
        energy = combination_bf(must, all, 3, field1, outfp="dryrun"+csv, monday_setting=monday_setting, recipe_name_reserve=recipe_name_reserve)
        esorted = sorted(energy)
        threshold1 = esorted[round(len(esorted)*0.99)]
        threshold5 = esorted[round(len(esorted)*0.95)]
        nmin_recalc = 500
        nmax_recalc = 5000
        threshold = esorted[max(min(len(esorted)-nmin_recalc, round(len(esorted)*0.95)), len(esorted)-nmax_recalc)]
        print(f"N  : {len(energy)}")
        print(f"max: {max(energy)}")
        print(f"min: {min(energy)}")
        print(f"1% : {threshold1}")
        print(f"5% : {threshold5}")
        print(f"recalc thresh : {threshold}")
        # print2(f"total length: {len(energy)}")
        # output only good results
        combination_bf(must, all, 100, field1, outfp=csv, TF_skip=[ e > threshold for e in energy], monday_setting=monday_setting, recipe_name_reserve=recipe_name_reserve)


def party_from_namelist(names):
    ret = []
    for p in PKS:
        if p in names:
            ret.append(PKS[p])
            PKS[p].show_ability()
    return ret
    
def party_from_tab_str(partystr):
    names = partystr.split("\t")
    ret = []
    for p in PKS:
        if p in names:
            ret.append(PKS[p])
            PKS[p].show_ability()
    return ret

def party_from_csv(partystr):
    names = partystr.split(",")
    ret = []
    for p in PKS:
        if p in names:
            ret.append(PKS[p])
            PKS[p].show_ability()
    return ret



class Field(object):
    def __init__(self, 
                 field_bonus=1, 
                 field_berry=[],
                 id_recipe_request=ID_RECIPE_CURRY,
                 pot_capacity=45,
                 recipe_lv_bonus=0.5):
        self.field_bonus = field_bonus            
        self.field_berry = field_berry    
        self.id_recipe_request = id_recipe_request    
        self.pot_capacity = round(pot_capacity*1.5) if GCT else pot_capacity
        self.extra_pot_capacity = 0
        self.recipe_lv_bonus = recipe_lv_bonus
        self.recipe_request = RECIPE[id_recipe_request]
        self.cooking_successful_rate = COOKING_SUCCESSFUL_RATE
    
    def reset_CSF_rate(self):
        self.cooking_successful_rate = COOKING_SUCCESSFUL_RATE
            

class Pokemon(object):

    # skill_misfire = 0
    
    
    def __init__(self, name, tribe, lv,
                 ingredients:list,
                 vitality, nature={"freq":0, "vitality":0, "exp":0, "ingr":0, "skill":0}, 
                 subskill={"skill":0, "speed":0, "ingr":0, "exp":0, "help_bonus":0, "berry":0, "inventory":0},
                 mainskill_lv=1,
                 n_evolve=0):
        pass
        self.name = name
        self.lv = max(lv,FORCE_PK_LV) if FORCE_PK_LV is not None else lv
        self.tribe = tribe
        self.pokemon = POKEMON[tribe]
        self.nature = nature
        self.subskill = {}
        for key, val in subskill.items():
            if isinstance(val, list):
                if self.lv >= 100:
                    self.subskill[key] = sum(val[:5])
                elif self.lv >= 75:
                    self.subskill[key] = sum(val[:4])
                elif self.lv >= 50:
                    self.subskill[key] = sum(val[:3])
                elif self.lv >= 25:
                    self.subskill[key] = sum(val[:2])
                elif self.lv >= 10:
                    self.subskill[key] = sum(val[:1])
                else:
                    self.subskill[key] = 0
            else:
                self.subskill[key] = val
        slvmax = 7 if self.pokemon['main_skill'] in [
                MS_CHARGE_STRENGTH_M,
                MS_CHARGE_STRENGTH_S,
                MS_CHARGE_STRENGTH_S_RANDOM,
                MS_CHARGE_STRENGTH_ACCUM,
                MS_DREAM_SHARD_MAGNET_S,
                MS_DREAM_SHARD_MAGNET_S_RANDOM,
                MS_INGREDIENT_MAGNET_S,
                MS_EXTRA_HELPFUL_S,
                MS_COOKING_POWER_UP_S,
                MS_SKILL_COPY] else 6
        slvadd = self.subskill["skill_lv_up"] if "skill_lv_up" in self.subskill else 0
        slvadd += EVENT_BONUS_SKILL_LV_UP['amount'] \
                if self.pokemon['kind'] in EVENT_BONUS_SKILL_LV_UP['kind'] \
                or self.pokemon['type'] in EVENT_BONUS_SKILL_LV_UP['type'] \
                else 0
        self.mainskill_lv = min(mainskill_lv + slvadd, slvmax)
        # fact = 2 if self.pokemon["berry"] in FIELD_BERRY else 1
        # self.berry_energy = round(max(BERRY[self.pokemon["berry"]]+self.lv-1, BERRY[self.pokemon["berry"]]*1.025**(self.lv-1)))*fact
        self.berry_energy = round(max(BERRY[self.pokemon["berry"]]+self.lv-1, BERRY[self.pokemon["berry"]]*1.025**(self.lv-1)))
        # self.base_freq = self.pokemon["freq"] - self.pokemon["freq"]*nature["freq"]*0.1
        nature["freq"] = nature["freq"] if 0 < nature["freq"] else 0.75 * nature["freq"] # 2025/03/27 お手スピダウン性格緩和
        self.base_freq = self.pokemon["freq"]*(1-(self.lv-1)*0.002)*(1-0.1*nature["freq"]) # サブスキル、おてぼは入ってない
        self.ss_faster = self.subskill["speed"] * 0.07
        # self.ingredients = ingredients
        # if self.pokemon['kind'] in EVENT_BONUS_ADDITIONAL_INGREDIENT['kind']:
        #     self.n_ingr = [ n + EVENT_BONUS_ADDITIONAL_INGREDIENT['amount'] for n in n_ingr]
        # else: 
        #     self.n_ingr = n_ingr
        """ ABC to 食材名, 食材数計算 """
        #"""
        ingr_A = self.pokemon["ingr"][0]
        ingr_B = self.pokemon["ingr"][1]
        ingr_C = self.pokemon["ingr"][2] if len(self.pokemon["ingr"]) > 2 else None
        # 第1食材
        ingr_1 = ingr_A
        n_ingr_1 = 2 if self.pokemon["type"] in ["食材", "オール"] else 1
        e_ingr_1 = FOOD[ingr_A]
        # 第2食材
        if ingredients[1]=="A":
            ingr_2 = ingr_A
            e_ingr_2 = FOOD[ingr_A]
        elif ingredients[1]=="B":
            ingr_2 = ingr_B
            e_ingr_2 = FOOD[ingr_B]
        # 第3食材
        if ingredients[2]=="A":
            ingr_3 = ingr_A
            e_ingr_3 = FOOD[ingr_A]
        elif ingredients[2]=="B":
            ingr_3 = ingr_B
            e_ingr_3 = FOOD[ingr_B]
        elif ingredients[2]=="C":
            ingr_3 = ingr_C
            e_ingr_3 = FOOD[ingr_C]
        self.ingredients = [ingr_1, ingr_2, ingr_3]
        bonus = EVENT_BONUS_ADDITIONAL_INGREDIENT['amount'] \
                if self.pokemon['kind'] in EVENT_BONUS_ADDITIONAL_INGREDIENT['kind']\
                or self.pokemon['type'] in EVENT_BONUS_ADDITIONAL_INGREDIENT['type'] \
                else 0
        self.n_ingr = [n_ingr_1+bonus, 
                       int(Decimal(e_ingr_1*n_ingr_1*2.25/e_ingr_2).quantize(Decimal('0'), rounding=ROUND_HALF_UP))+bonus, 
                       int(Decimal(e_ingr_1*n_ingr_1*3.60/e_ingr_3).quantize(Decimal('0'), rounding=ROUND_HALF_UP))+bonus]
        # """
        self.n_evolve = n_evolve
        self.skill_standby = 0
        if self.pokemon['type'] in ["きのみ", "オール"]:
            if self.subskill['berry']!=0:
                self.n_berry = 3
            else:
                self.n_berry = 2
        else:
            if self.subskill['berry']!=0:
                self.n_berry = 2
            else:
                self.n_berry = 1
        self.vitality = vitality
        
        fact = EVENT_BONUS_SKILL_TRIGGER['fact'] \
                if self.pokemon['kind'] in EVENT_BONUS_SKILL_TRIGGER['kind'] \
                or self.pokemon['type'] in EVENT_BONUS_SKILL_TRIGGER['type'] \
                else 1
        self.skill_prob = PROBABILITY[tribe]['skill']/100 * (1 + 0.18*self.subskill['skill']) * (1+0.2*nature["skill"]) * fact
        self.ingr_prob = PROBABILITY[tribe]['ingr']/100 * (1 + 0.18*self.subskill['ingr']) * (1+0.2*nature["ingr"])
        if "inventory" in self.subskill:
            self.inventory = INVENTORY[tribe] + 6*self.subskill['inventory'] + 5*self.n_evolve
        else:
            self.inventory = INVENTORY[tribe] + 5*self.n_evolve
        if GCT:
            self.inventory = round(self.inventory*1.5)

        self.n_skill_activated = 0
        self.cumulated_energy = 0
        self.cumulated_ingredients = {}
        self.misfire_counter = 0
        self.extra_help_energy = 0
        self.extra_help_ingredients = {}
        if self.nature["vitality"] < 0:
            self.recov_fact = 0.88
        elif self.nature["vitality"] > 0:
            self.recov_fact = 1.2
        else:
            self.recov_fact = 1.0
        if self.lv >= 60:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + sum(self.n_ingr) * self.ingr_prob / 3
        elif self.lv >= 30:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + sum(self.n_ingr[0:2]) * self.ingr_prob / 2
        else:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + self.n_ingr[0] * self.ingr_prob 
        
    def recovery(self, vitality):
        self.vitality += vitality
    
    def skill_activate_probability(self, n_help):
        return 1 - (1-self.skill_prob)**n_help

    def skill_activate_probability_n_times(self, n_activation, n_help):
        return comb(n_help, n_activation)*\
                    self.skill_prob**n_activation*\
                    (1-self.skill_prob)**(n_help-n_activation)
    
    def skill_activate_probability_two_times(self, n_help):
        # (1回以上発動) - (一回だけ発動)
        return self.skill_activate_probability(n_help) - self.skill_activate_probability_n_times(1, n_help)

    def skill_activate_probability_above_n_times(self, n_activation, n_help):
        # n_helpを丸めないとnanになる
        n_help = round(n_help)
        # 1 - CDF(n-1) は n 回以上当たる確率
        probability = 1 - binom.cdf(n_activation-1, n_help, self.skill_prob)
        return probability

    def work(self, duration, party, field:Field):
        # count helping_bonus
        n_help_bonus = sum([pk.subskill['help_bonus'] for pk in party])

        nh = self.n_times_help(duration, n_help_bonus)

        if nh * self.n_item_single_help > self.inventory:
            nh_extra = nh - self.inventory / self.n_item_single_help 
            nh = self.inventory / self.n_item_single_help 
            print3(f"({self.name}, inventory overflowed)", end="")
        else:
            nh_extra = 0

        # 食材回数
        # print2(f"    n_help:{nh:.2f}")
        nh_i = nh * self.ingr_prob
        for ing in self.n_ingredients(nh_i):
            # print2(f"    {ing['kind']}: {ing['amount']:.2f}")
            if ing['kind'] in self.cumulated_ingredients:
                self.cumulated_ingredients[ing['kind']] += ing['amount']
            else:
                self.cumulated_ingredients[ing['kind']] = ing['amount']
        # きのみ回数
        nh_b = nh * (1-self.ingr_prob) + nh_extra
        # 合計きのみエナジー
        fact = 2 if self.pokemon["berry"] in field.field_berry else 1
        energy_berry = round(nh_b*self.n_berry*self.berry_energy*fact*field.field_bonus,2)
        self.cumulated_energy += energy_berry
        # print2(f"    きのみ {nh_b:.2f} {energy_berry:.2f}")
    
        # skill
        p1 = self.skill_activate_probability_n_times(1, nh)
        # p2 = self.skill_activate_probability_above_n_times(2, nh)
        p2 = self.skill_activate_probability_two_times(nh)
        # print2(f"skillprob {p1:.2f} {p2:.2f}")
        x = random.random() 
        if x < p2 and (self.pokemon['type'] in ['スキル', 'オール']) and ENABLE_SKILL_DOUBLE_STANDBY:
            # activated twice 
            self.skill_standby = 2
            self.misfire_counter = 0
        elif x < p1 + p2:
            # activated once
            self.skill_standby = 1
            self.misfire_counter = 0
        else:
            # miss fire
            self.skill_standby = 0
            self.misfire_counter += nh
        
        # is_skill_activated =  random.random() <= self.skill_activate_probability(nh)
        # if is_skill_activated: 
        #     # print2(f"[{self.name}] skill standby OK !! ID:{self.pokemon['main_skill']}")
        #     self.skill_standby = True
        #     # self.n_skill_activated += 1
        #     self.misfire_counter = 0
        # else:
        #     self.misfire_counter += nh
    
        return energy_berry, self.n_ingredients(nh_i)
    
    def n_times_work(self, n, field:Field):
        ret_igr = {}
        ret_egy = 0
        for igr in self.n_ingredients(n*self.ingr_prob):
            if igr['kind'] in ret_igr:
                ret_igr[igr['kind']] += igr['amount']
            else:
                ret_igr[igr['kind']] = igr['amount']
        fact = 2 if self.pokemon["berry"] in field.field_berry else 1
        ret_egy += n*(1-self.ingr_prob)*self.n_berry*self.berry_energy*fact*field.field_bonus
        return ret_egy, ret_igr
    

    def skill_exec(self, party:list, field:Field, main_skill_id:int=None, isCalledRecursively=False):
        energy_extra = 0
        ingredients_extra = {}
        recovery = [0, 0, 0, 0, 0]
        if main_skill_id is None:
            main_skill_id = self.pokemon['main_skill'] 
        # if self.skill_standby:
        for _ in range(self.skill_standby):
            # print2(f"skill activated!! ID:{main_skill_id}")
            # 元気チャージ
            if main_skill_id == MS_ENERGY_CHARGE_S:
                print4(f"[SKILL] ({self.name}): MS ENERGY CHARGE S (lv{self.mainskill_lv})", end="  ")
                table = [12.0, 16.2, 21.2, 26.6, 33.6, 43.4, 43.4]
                extra = table[self.mainskill_lv-1]*self.recov_fact
                self.vitality = min(150, self.vitality+extra)
                print4(f"+{extra}")

            if main_skill_id == MS_ENERGY_CHARGE_MOONLIGHT:
                print4(f"[SKILL] ({self.name}): ENERGY CHARGE MOONLIGHT (lv{self.mainskill_lv})", end="  ")
                table = [12.0, 16.2, 21.2, 26.6, 33.6, 43.4, 43.4]
                extra = table[self.mainskill_lv-1]*self.recov_fact
                self.vitality = min(150, self.vitality+extra)
                print4(f"{self.name} +{extra}", end="  ")

                if random.random() <= MS_ENERGY_CHARGE_MOONLIGHT_SUCCESS_PROB:
                    table2 = [6, 7, 10, 13, 17, 22, 22]
                    idpk = random.randint(0,len(party)-1)
                    selected_pk = party[idpk]
                    extra2 = table2[self.mainskill_lv-1]*selected_pk.recov_fact
                    selected_pk.vitality = min(selected_pk.vitality + extra2,150)
                    print4(f"{selected_pk.name} +{extra2}", end="")
                print4(" ")

                
            # エナジーチャージSM
            if main_skill_id == MS_CHARGE_STRENGTH_S:
                print4(f"[SKILL] ({self.name}): MS CHARGE STRENGTH S (lv{self.mainskill_lv})", end="  ")
                extra = [440, 569, 785, 1083, 1496, 2056, 3002][self.mainskill_lv-1]*field.field_bonus
                energy_extra += extra
                print4(f"+{extra}")
            if main_skill_id == MS_CHARGE_STRENGTH_S_RANDOM:
                print4(f"[SKILL] ({self.name}): MS CHARGE STRENGTH S RANDOM (lv{self.mainskill_lv})", end="  ")
                table = [[200, 800],
                        [285, 1138],
                        [393, 1570],
                        [542, 2166],
                        [748, 2992],
                        [1033, 4132],
                        [1501, 6004]]
                extra = sum(table[self.mainskill_lv-1])/2*field.field_bonus
                energy_extra += extra
                print4(f"+{extra}")
                
            if main_skill_id == MS_CHARGE_STRENGTH_M:
                print4(f"[SKILL] ({self.name}): MS CHARGE STRENGTH M (lv{self.mainskill_lv})", end="  ")
                extra = [880, 1251, 1726, 2383, 3290, 4546, 6409][self.mainskill_lv-1]*field.field_bonus
                energy_extra += extra
                print4(f"+{extra}")

            if main_skill_id == MS_CHARGE_STRENGTH_ACCUM:
                print4(f"[SKILL] ({self.name}): CHARGE STRENGTH ACCUM (lv{self.mainskill_lv})", end="  ")
                # TODO 実装する
                pass

            # 夢のカケラゲット
            if main_skill_id == MS_DREAM_SHARD_MAGNET_S:pass
            if main_skill_id == MS_DREAM_SHARD_MAGNET_S_RANDOM:pass
            # 料理チャンス
            if main_skill_id == MS_TASTY_CHANCE:
                print4(f"[SKILL] ({self.name}): TASTY CHANCE S (lv{self.mainskill_lv})", end="  ")
                table = [4,5,6,7,8,10, 10]
                print4(f"{field.cooking_successful_rate*100}+{table[self.mainskill_lv-1]}")
                field.cooking_successful_rate = min(70, int(field.cooking_successful_rate*100)+table[self.mainskill_lv-1])/100
            # 料理パワーアップ
            if main_skill_id == MS_COOKING_POWER_UP_S:
                print4(f"[SKILL] ({self.name}): COOKING POWER UP S (lv{self.mainskill_lv})", end="  ")
                table = [7,10,12,17,22,27,31]
                print4(f"{field.pot_capacity+field.extra_pot_capacity}+{table[self.mainskill_lv-1]}")
                field.extra_pot_capacity += table[self.mainskill_lv-1]
            # 食材ゲットS
            if main_skill_id == MS_INGREDIENT_MAGNET_S:
                print4(f"[SKILL] ({self.name}): INGREDIENT MAGNET S (lv{self.mainskill_lv})", end="  ")
                n = [6, 8, 11, 14, 17, 21, 24][self.mainskill_lv-1]
                food_ids = []
                while len(food_ids)<3:
                    rand = random.randint(0,len(FOOD.items())-1)
                    if rand in food_ids:
                        continue
                    else:
                        food_ids.append(rand)
                for fid in food_ids:
                    key = list(FOOD.keys())[fid] # key
                    print4(f"{key}: {n/3:2f}", end=", ")
                    if key in ingredients_extra:
                        ingredients_extra[key] += n/3
                    else:
                        ingredients_extra[key] = n/3
                else:
                    print4("")
                

            # 元気オール
            if main_skill_id == MS_ENERGY_4_EVERYONE:
                print4(f"[SKILL] ({self.name}): ENERGY FOR EVERYONE (lv{self.mainskill_lv})", end="  ")
                amount = [5,7,9,11,15,18, 18]
                print4(f"+{amount[self.mainskill_lv-1]}", end="")
                for pkid, pk in enumerate(party):
                    # recovery[pkid] = min(pk.vitality + amount[self.mainskill_lv-1]*pk.recov_fact, 150) - pk.vitality
                    pk.vitality = min(pk.vitality + amount[self.mainskill_lv-1]*pk.recov_fact, 150)
                    # print4(f"{pk.name}:{pk.vitality-amount[self.mainskill_lv-1]:.1f}-->{pk.vitality:.1f}", end=", ")
                else:
                    print4("")
            # 元気エール
            if main_skill_id == MS_ENERGIZING_CHEER_S:
                print4(f"[SKILL] ({self.name}): MS ENERGIZING CHEER S (lv{self.mainskill_lv})", end="  ")
                amount = [14, 17.1, 22.5, 28.8, 38.2, 50.6, 50.6]

                ## 重み付け選択の場合
                # vitalityでソート
                sorted_pks = sorted(party, key=lambda pk: pk.vitality)
                # 確率のリスト
                probabilities = [0.5, 0.3, 0.1, 0.1, 0.1][0:len(sorted_pks)]
                # オブジェクトを確率的に選択
                selected_pk = random.choices(sorted_pks, weights=probabilities, k=1)[0]
                
                ## 完全ランダム選択の場合
                # idpk = random.randint(0,len(party)-1)
                # selected_pk = party[idpk]
                
                selected_pk.vitality = min(selected_pk.vitality + amount[self.mainskill_lv-1]*selected_pk.recov_fact,150)
                print4(f"{selected_pk.name}:{selected_pk.vitality-amount[self.mainskill_lv-1]*selected_pk.recov_fact:.1f}-->{selected_pk.vitality:.1f}")
            
            # お手伝いサポート
            if main_skill_id == MS_EXTRA_HELPFUL_S:
                print4(f"[SKILL] ({self.name}): EXTRA HELPFUL (lv{self.mainskill_lv})", end="  ")
                table = [5,6,7,8,9,10,11]
                pk = party[random.randint(0,len(party)-1)]
                e, additinal_igr = pk.n_times_work(table[self.mainskill_lv-1], field)
                # 通常エナジーへの加算
                energy_extra += e
                # ストック済みエナジーへの加算
                isPkNoTaps = pk.pokemon['main_skill'] not in [MS_EXTRA_HELPFUL_S, MS_HELPER_BOOST, MS_ENERGY_4_EVERYONE]
                self.extra_help_energy += e if isPkNoTaps else 0
                for key, n in additinal_igr.items():
                    # 通常食材への加算
                    if key in ingredients_extra:
                        ingredients_extra[key] += n
                    else:
                        ingredients_extra[key] = n
                    # ストック済み食材へ加算
                    if key in self.extra_help_ingredients:
                        self.extra_help_ingredients[key] += n if isPkNoTaps else 0
                    else:
                        self.extra_help_ingredients[key] = n if isPkNoTaps else 0
                print4(f"({pk.name}) berry energy: {e:.1f}, ingredients: {additinal_igr}")

            # ゆびをふる
            if main_skill_id == MS_METRONOME:
                print4(f"[SKILL] ({self.name}): METRONOME (lv{self.mainskill_lv})")
                # スキル発動
                self.skill_exec(party, field, main_skill_id=random.randint(1, N_KIND_MS+1),
                                isCalledRecursively=True)
            
            # お手伝いブースト
            if main_skill_id == MS_HELPER_BOOST:
                table = [
                    [2,2,3,4,6],
                    [3,3,4,5,7],
                    [3,3,5,6,8],
                    [4,4,6,7,9],
                    [4,5,7,8,10],
                    [5,6,8,9,11],
                    [5,6,8,9,11],
                ]
                # count same kind pokemons    
                tmp = []
                for pk in party:
                    if pk.pokemon['berry'] == self.pokemon['berry']\
                            and (not pk.tribe in tmp): 
                        tmp.append(pk.tribe)
                        
                n_extra = table[self.mainskill_lv-1][len(tmp)-1]
                print4(f"[SKILL] ({self.name}): HELPER BOOST (lv{self.mainskill_lv})")
                print4(f"    n same berry but different tribe: {len(tmp)} ({tmp})")
                print4(f"    n extra help per pokemon: {n_extra}")

                for pk in party:
                    pk:Pokemon
                    e, additinal_igr = pk.n_times_work(n_extra, field)
                    # 通常エナジーへの加算
                    energy_extra += e
                    # ストック済みエナジーへの加算
                    isPkNoTaps = pk.pokemon['main_skill'] not in [MS_EXTRA_HELPFUL_S, MS_HELPER_BOOST, MS_ENERGY_4_EVERYONE]
                    self.extra_help_energy += e if isPkNoTaps else 0
                    
                    for key, n in additinal_igr.items():
                        # 通常食材への加算
                        if key in ingredients_extra:
                            ingredients_extra[key] += n
                        else:
                            ingredients_extra[key] = n
                        # ストック済み食材へ加算
                        if key in self.extra_help_ingredients:
                            self.extra_help_ingredients[key] += n if isPkNoTaps else 0
                        else:
                            self.extra_help_ingredients[key] = n if isPkNoTaps else 0
                    print4(f"      ({pk.name}) berry energy: {e:.1f}, ingredients: {sum(additinal_igr.values()):.2f}")
                    
                    # for igr in pk.n_ingredients(n_extra*pk.ingr_prob):
                    #     if igr['kind'] in ingredients_extra:
                    #         ingredients_extra[igr['kind']] += igr['amount']
                    #     else:
                    #         ingredients_extra[igr['kind']] = igr['amount']
                    # energy_extra += n_extra*(1-pk.ingr_prob)*pk.n_berry*pk.berry_energy*field.field_bonus
                    # print4(f"[{pk.name}]berry energy: {n_extra*(1-pk.ingr_prob)*pk.n_berry*pk.berry_energy*field.field_bonus:.1f}, ingredients: {sum([i['amount']for i in pk.n_ingredients(n_extra*pk.ingr_prob)]):.2f}")
                
                print4(f"    TOTAL EXTRA ENERGY:{energy_extra:.1f}")
                print4(f"    EXTRA INGREDIENTS:{ingredients_extra}")


            # Disguise (Berry Burst)
            if main_skill_id == MS_BERRY_BURST:
                print4(f"[SKILL] ({self.name}): Disguise (Berry Burst) (lv{self.mainskill_lv})")
                table1 = [8, 10, 15, 17, 19, 21, 21]
                table2 = [1, 2, 2, 3, 4, 5, 5]
                fact2 = 1
                if random.random() <= MS_BERRY_BURST_SUCCESS_PROB:
                    fact2 = 3
                    print4(f" SUCCESSFULL !!")
                for pk in party:
                    fact = 2 if pk.pokemon["berry"] in field.field_berry else 1
                    e = table2[self.mainskill_lv-1]*pk.berry_energy*fact*fact2
                    print5(f"    {pk.name} n:{table2[self.mainskill_lv-1]} e:{e}")
                    energy_extra += e*field.field_bonus

                fact = 2 if self.pokemon["berry"] in field.field_berry else 1
                e = (table1[self.mainskill_lv-1]-table2[self.mainskill_lv-1])*self.berry_energy*fact*fact2
                print5(f"    {self.name} n:{table1[self.mainskill_lv-1]-table2[self.mainskill_lv-1]} e:{e}")
                energy_extra += e
                print4(f"    TOTAL EXTRA ENERGY:{energy_extra:.1f}")
            
            # Skill Copy
            if main_skill_id == MS_SKILL_COPY:
                print4(f"[SKILL] ({self.name}): SKILL COPY (lv{self.mainskill_lv})")
                skills = []
                for pp in party:
                    if id(pp)==id(self):continue
                    skills.append(MS_CHARGE_STRENGTH_S if pp.pokemon['main_skill'] is MS_SKILL_COPY else pp.pokemon['main_skill'])
                # スキル発動
                self.skill_exec(party, field, main_skill_id=skills[random.randint(0, len(skills)-1)],
                                isCalledRecursively=True)
            
            # lunar bressing
            if main_skill_id == MS_LUNAR_BRESSING:
                print4(f"[SKILL] ({self.name}): LUNAR BRESSING (lv{self.mainskill_lv})")

                # 元気エール
                amount = [3, 4, 5, 7, 9, 11, 11]
                print4(f"+{amount[self.mainskill_lv-1]}")
                for pkid, pk in enumerate(party):
                    pk.vitality = min(pk.vitality + amount[self.mainskill_lv-1]*pk.recov_fact, 150)

                # きのみ獲得
                table = [
                    [1,1,1,1,2],
                    [1,1,1,2,3],
                    [1,1,2,3,4],
                    [1,2,2,3,5],
                    [1,2,3,5,7],
                    [1,2,4,6,9],
                    [1,2,4,6,9],
                ]
                table2 = [
                    [5,7,9,12,14],
                    [9,12,15,16,19],
                    [13,17,18,20,24],
                    [17,19,25,28,29],
                    [21,24,27,28,30],
                    [25,29,30,31,32],
                    [25,29,30,31,32],
                ]
                
                # count same kind pokemons    
                tmp = []
                for pk in party:
                    if pk.pokemon['berry'] == self.pokemon['berry']\
                            and (not pk.tribe in tmp): 
                        tmp.append(pk.tribe)        
                n_extra_berry = table[self.mainskill_lv-1][len(tmp)-1]
                n_extra_berry_self = table2[self.mainskill_lv-1][len(tmp)-1]
                
                # add energy by extra berries
                for pk in party:
                    fact = 2 if pk.pokemon["berry"] in field.field_berry else 1
                    if id(pk)==id(self):
                        e = n_extra_berry_self*pk.berry_energy*fact*field.field_bonus
                        print5(f"    {pk.name} n:{n_extra_berry_self} e:{e}")
                    else:
                        e = n_extra_berry*pk.berry_energy*fact*field.field_bonus
                        print5(f"    {pk.name} n:{n_extra_berry} e:{e}")
                    energy_extra += e

            # Nightmare
            if main_skill_id == MS_NIGHTMARE:
                extra = [2640, 3753, 5178, 7149, 9870, 13638, 13638][self.mainskill_lv-1]*field.field_bonus
                print4(f"[SKILL] ({self.name}): NIGHTMARE (lv{self.mainskill_lv}) +{extra}")
                energy_extra += extra
                for pkid, pk in enumerate(party):
                    if pk.pokemon['kind']!=PK_AKU:
                        new_vit = max(pk.vitality - 12, 0)
                        # print4(f"{pk.name}:{pk.vitality:.1f}-->{new_vit:.1f}")
                        pk.vitality = new_vit
            
            if not isCalledRecursively:
                self.n_skill_activated += 1

            # add to self
            self.cumulated_energy += energy_extra
            for ing in ingredients_extra:
                if ing in self.cumulated_ingredients:
                    self.cumulated_ingredients[ing] += ingredients_extra[ing]
                else:
                    self.cumulated_ingredients[ing] = ingredients_extra[ing]

        self.skill_standby = 0
        return energy_extra, ingredients_extra, recovery


    
    def n_times_help(self, duration, n_help_bonus=0, dry_run=False):
        vitality = self.vitality
        # 回復量は時間ごとに均等に分け与える
        t_elapsed = 0
        n = 0
        actual_freq = math.floor(self.base_freq * (1-(0.05*n_help_bonus + self.ss_faster)))
        if GCT:
            actual_freq /= 1.2
        # print4(f"actual freq: {actual_freq//60}:{actual_freq - (actual_freq//60)*60}")
        vital_bf_stp = 0
        for ii in [(80, 0.45), (60, 0.52), (40, 0.58), (20, 0.66), (0,1)]:
            while vitality >= ii[0] and t_elapsed < duration:
                t_elapsed += actual_freq*ii[1]
                # print4(f"... dt now:{actual_freq*ii[1]}")
                # print4(f"... reduced vitality/dt:{actual_freq*ii[1]/600}")
                vital_bf_stp = vitality
                if (vitality - actual_freq*ii[1]/600) < 0:
                    vitality = 0
                else:
                    vitality -= actual_freq*ii[1]/600

                n += 1
            else:
                if not t_elapsed < duration: 
                    break
        # 端数処理
        # print4("end time reached")
        stp_len_now = actual_freq*ii[1]
        excess_t = t_elapsed - duration
        tfrom_bfstp_completed = duration - (t_elapsed-stp_len_now)
        ## n_help
        n = n - excess_t/stp_len_now
        ## vitality
        if (vital_bf_stp - tfrom_bfstp_completed/600) <= 0:
            vitality = 0
        else: 
            vitality = vital_bf_stp - tfrom_bfstp_completed/600
        
        if not dry_run: self.vitality = vitality
        
        # print4(f'--- time elapsed: {duration/3600:.2f}h, finished help: {n}')
        return n
    
    def n_ingredients(self, n_help):
        if self.lv <30:
            return [{'kind':self.ingredients[0], 'amount':round(n_help * self.n_ingr[0],2)}]
        elif self.lv >=30 and self.lv < 60:
            return [{'kind':self.ingredients[0], 'amount':round(n_help * self.n_ingr[0]/2,2)},
                    {'kind':self.ingredients[1], 'amount':round(n_help * self.n_ingr[1]/2,2)}]
        else:
            return [{'kind':self.ingredients[0], 'amount':round(n_help * self.n_ingr[0]/3,2)},
                    {'kind':self.ingredients[1], 'amount':round(n_help * self.n_ingr[1]/3,2)},
                    {'kind':self.ingredients[2], 'amount':round(n_help * self.n_ingr[2]/3,2)}]

    def info(self):
        print4(f"[{self.name}]")
        # print4(f"berry_energy: {self.berry_energy}")
        # print4(f"lv: {self.lv}")
        # print4(f"base_freq: {self.base_freq}")
        # print4(f"ingredients: {self.ingredients}")
        print4(f"    vitality: {self.vitality:.2f}")
        # print4(f"ss_faster: {self.ss_faster}")
        print4(f"cumulated_energy: {self.cumulated_energy}")

    def show_ability(self):
        print2(f"{self.name}({self.tribe})")
        m = (self.base_freq*(1-self.ss_faster))//60
        s = (self.base_freq*(1-self.ss_faster))-60*m
        print2(f"            freq: {m:.0f}:{s:.0f}")
        if GCT:
            m = (self.base_freq*(1-self.ss_faster)/1.2)//60
            s = (self.base_freq*(1-self.ss_faster)/1.2)-60*m
            print2(f"        GCT freq: {m:.0f}:{s:.0f}")
        print2(f"    berry energy: {self.berry_energy}")
        print2(f"        skill lv: {self.mainskill_lv}")
        print2(f"           skill: {self.skill_prob*100:.1f}%")
        print2(f"     ingredients: {self.ingredients}")
        print2(f"   n ingredients: {self.n_ingr}")
        print2(f" ingredient prob: {self.ingr_prob*100:.1f}%")
        print2(f"       inventory: {self.inventory}")
        print2(f" N item / a help: {self.n_item_single_help}")

def ryori(bag, field:Field, non_essential_ingrs:list=None, rcp_primary=None, 
          essential_ingrs:list=None, n_essential_igrs:list=None, isWeekend=False):
    # カレー、デザート、サラダそれぞれ、料理を優先順位でソートしたリストを作っておく。
    # 上から順番にあたって、作れる料理が出た時点で料理を行う
    # non_essential_ingrsがある場合、追加食材選定時に優先的に使用される
    # essential_ingrsとn_essential_ingrsがある場合、必要数が使用されず確保される
    for recipe in field.recipe_request:
        
        # そもそも鍋容量が足りているのかのチェックを行う
        if (field.pot_capacity+field.extra_pot_capacity) < recipe["n"]:
            # なべ容量不足のときは次のレシピを当たる
            continue

        # このレシピの、
        for igr, a in  zip(recipe['ingredients'], recipe['amounts']):
            # 食材について、第１段階のチェック。そもそも足りているか。
            if igr in bag and bag[igr] >= a:
                pass
            else:
                # 材料不足のときは次のレシピを当たる
                break
            # 第一段階がOKの場合、この食材の量についてさらにチェックする
            if rcp_primary is not None:
                if recipe["name"] not in rcp_primary:
                    # 優先レシピに含まれない場合は材料を確保しつつ、なお作れるかの判定を行う。
                    if essential_ingrs is not None and n_essential_igrs is not None:
                        breaks = False
                        for i , ess_igr in enumerate(essential_ingrs):
                            if ess_igr == igr:
                                # 優先レシピに使われている食材だった場合には確保すべき量+このレシピでの必要量がBAGにない場合は次のレシピを当たる
                                if bag[igr] < a + n_essential_igrs[i]:
                                    breaks = True
                                    break
    
                        if breaks:
                            break
                        # 優先レシピには使われていない食材だった場合はチェック不要
                    # 優先食材、優先食材料が特に指定されていない場合はそのまま作る
                # 優先レシピに含まれる場合は食材量のチェックは不要
            # 優先レシピが特に指定されていない場合はそのまま作る

        else:
            # 一つrecipeがヒットしたらループはストップする
            lv = max(FORCE_RECIPE_LV, recipe["lv"]) # 強制的にもレベル設定できる
            print4(f"RECIPE: {recipe['name']}(lv{lv})  POT CAPACITY: {field.pot_capacity+field.extra_pot_capacity}  TASTY CHANCE: {field.cooking_successful_rate*100}%")
            print4("  essentials:")
            n_used = 0
            for igr, a in  zip(recipe['ingredients'], recipe['amounts']):
                print4(f"    {igr}: {bag[igr]:.2f} --> {bag[igr]-a:.2f}")
                bag[igr] -= a
                n_used += a
            
            e1 = recipe["base_energy"] + round(recipe["base_energy"]*RECIPE_LV_BONUS_TABLE[lv])  
            # 追加食材の選定
            print4("  additional1:")
            if non_essential_ingrs is None:
                # 最も多く余っている食材一種類からつかう
                additional_energy, n = choose_additional_ingredients(bag, (field.pot_capacity+field.extra_pot_capacity)-recipe["n"])
            else:
                # non_essential_ingrsリストに含まれる食材からつかう
                additional_energy, n = choose_additional_ingredients2(bag, (field.pot_capacity+field.extra_pot_capacity)-recipe["n"], non_essential_ingrs)
            total_energy = (additional_energy + e1) * field.field_bonus * EVENT_BONUS_RECIPE_FACT
            # 大成功かどうか
            info = ""
            if random.random() <= field.cooking_successful_rate:
                weekendBonus = 1.5 if isWeekend else 1.0
                total_energy = total_energy*COOKING_SUCCESSFUL_FACT*weekendBonus
                info = "SUCCESSFUL !! "
                field.reset_CSF_rate()

            print4(f"ENERGY: {total_energy}, number of ingrs used: {n+n_used}  {info}")
            
            # 鍋リセット
            field.extra_pot_capacity = 0
        
            return recipe["name"]+f"({lv})", total_energy
    # 作れるレシピがない場合は料理スキップする
    return "skip", 0


def recipe_bonus(recipe):

    if recipe["n"] >= 87:
        b = 1.61
    elif recipe["n"] >= 62:
        b = 1.48
    elif recipe["n"] >= 53:
        b = 1.35
    elif recipe["n"] >= 30:
        b = 1.25
    elif recipe["n"] >= 22:
        b = 1.17
    elif recipe["n"] >= 14:
        b = 1.11
    else:
        b = 1.07
    
    if recipe["name"]=="はなびらのまいチョコタルト":
        b = 1.25
    if recipe["name"]=="めいそうスイートサラダ":
        b = 1.48
    if recipe["name"]=="だいばくはつポップコーン":
        b = 1.35
    if recipe["name"]=="みだれづきコーンサラダ":
        b = 1.25
    if recipe["name"]=="ニンジャカレー":
        b = 1.48
    if recipe["name"]=="ピヨピヨパンチ辛口カレー":
        b = 1.35
    if recipe["name"]=="ニンジャサラダ":
        b = 1.48
    if recipe["name"]=="はやおきコーヒーーゼリー":
        b = 1.35

    return b



def choose_additional_ingredients(bag, n):
    """
    define.N_SAVE_ESSENTIAL: この個数は最低限残す
    """
    tmp = ""
    additional_energy = 0
    n_have = 0
    n_used = 0
    for igr in bag:
        if bag[igr] > n_have:
            tmp = igr
            n_have = bag[igr]
    if tmp=="":
        return additional_energy, n_used
    
    if (bag[tmp]-N_SAVE_ESSENTIAL)-n >=0:
        additional_energy = FOOD[tmp]*n
        print4(f"    {tmp}: {bag[tmp]:.2f} --> {bag[tmp]-n:.2f}")
        n_used = n
        bag[tmp] = bag[tmp]-n
    else:
        additional_energy = FOOD[tmp]*(bag[tmp]-N_SAVE_ESSENTIAL)
        print4(f"    {tmp}: {bag[tmp]:.2f} --> {N_SAVE_ESSENTIAL}")
        n_used += bag[tmp]-N_SAVE_ESSENTIAL
        bag[tmp] = N_SAVE_ESSENTIAL

    return additional_energy, n_used

def choose_additional_ingredients2(bag, n, non_essentials:list):
    # n_saveはnon_essentials以外の食材の使用時、に最低これだけは残す数
    # non_essentialsの食材を優先的に使用する
    additional_energy = 0
    n_required = n
    n_used = 0
    for igr in non_essentials:
        if igr in bag:
            if bag[igr] >= n_required:
                additional_energy += FOOD[igr]*n_required
                print4(f"    {igr}: {bag[igr]:.2f} --> {bag[igr]-n_required:.2f}")
                bag[igr] -= n_required
                n_used += n_required
                n_required = 0
                break
            else:
                additional_energy += FOOD[igr]*bag[igr]
                n_required -= bag[igr]
                print4(f"    {igr}: {bag[igr]:.2f} --> 0")
                n_used += bag[igr]
                bag[igr] = 0
    print4(f"  additional2:")
    if n_required > 0:
        # non_essentialsの食材を使い切ってしまった場合、最も多く余っている食材を使う。このときN_SAVE_ESSENTIALだけは残すようにする
        additional2, n2 = choose_additional_ingredients(bag, n_required)
        additional_energy += additional2
        n_used += n2
        n_required -= n2
        if n_required-n2 > 0:
            # non_essentialsの食材を使い切ってしまった場合、最も多く余っている食材を使う。このときN_SAVE_ESSENTIALだけは残すようにする
            additional2, n2 = choose_additional_ingredients(bag, n_required)
            additional_energy += additional2
            n_used += n2

    return additional_energy, n_used


            

def list_up_possible_recipe(ing, field:Field, party, recipe_name_reserve=""):
    """
    recipe_name_reserve: （このレシピが今週の料理のレパートリーに含まれる場合のみ）このレシピの食材を追加食材として使わない。
    """
    ing_essential = []
    n_ing_essential = []
    ing_additional = []
    recipe_considered = []
    count = 0

    has_cooking_power_up = False
    for pk in party:
        if pk.pokemon['main_skill'] == MS_COOKING_POWER_UP_S:
            has_cooking_power_up = True

    for r in field.recipe_request:
        if recipe_name_reserve!=r['name'] and \
                sum(r['amounts']) > field.pot_capacity and not has_cooking_power_up:
            continue
        
        for i in r["ingredients"]:
            if recipe_name_reserve==r['name']:
                continue
            elif i in ing:
                continue
            else:
                break
        else:
            for igr, amo in zip(r['ingredients'],r['amounts']):
                if igr not in ing_essential:
                    ing_essential.append(igr)
                    n_ing_essential.append(amo)
                else:
                    for ii, ig, in enumerate(ing_essential):
                        if ig==igr:
                            if amo > n_ing_essential[ii]:
                                n_ing_essential[ii] = amo
            recipe_considered.append(r['name'])
            print4(f"recipe matched: {r['name']} {r['ingredients']} {r['base_energy']}")
            count += 1
            if count >= MAX_N_RECIPE_CONSIDER:
                break
    
    for f in FOOD:
        if f in ing_essential:
            pass
        else:
            ing_additional.append(f)
    return ing_essential, ing_additional, recipe_considered, n_ing_essential



def one_week(party, field:Field, cooks=True, ing_additional=None, rcp_primary=None,
             ing_essential=None, n_ing_essential=None, bag=None):
    # reset counter
    # for p in party: 
    #     p.cumulated_energy = 0
    #     p.cumulated_ingredients = {}
    #     p.n_skill_activated = 0

    # BAGを引数から受け取る。指定がなければDEFAULT_BAGをコピー
    BAG = bag.copy() if bag else DEFAULT_BAG.copy()
    
    ENERGY = 0
    ENERGY_RECIPE = 0
    TOTAL_IGR_AQUIRED = {}
    RECIPE_MADE = []
    RECIPE_MADE_ENG = []

    # for dt in [9600]*5+[3600*8]:
    time = 3600 * 8
    for day in range(7):
        # for dt in [1800]*31+[30600]:
        # for dt in [18600]*3+[30600]:
        ryori_eaten = 0 
        for dt in [1860*5]*6+[30600]:

            print4(f"\n*** TIME: {time//(3600*24)}d {time%(3600*24)/3600:.2f}h")

            # 働く前に料理
            # 料理
            if cooks:
                if ryori_eaten==0 and (time%(3600*24))>3600*4:
                    # 朝
                    print4("-- 朝料理", end="  ")
                    ryori_eaten += 1
                    r, e= ryori(BAG, field, non_essential_ingrs=ing_additional, rcp_primary=rcp_primary,
                                essential_ingrs=ing_essential, n_essential_igrs=n_ing_essential,
                                isWeekend=(day==6))
                    ENERGY_RECIPE += e
                    RECIPE_MADE.append(r)
                    RECIPE_MADE_ENG.append(e)
                    if e>0: vitality_recovery(party)
                if ryori_eaten==1 and (time%(3600*24))>3600*12:
                    print4("-- 昼料理", end="  ")
                    # 昼
                    ryori_eaten += 1
                    r, e= ryori(BAG, field, non_essential_ingrs=ing_additional, rcp_primary=rcp_primary,
                                essential_ingrs=ing_essential, n_essential_igrs=n_ing_essential,
                                isWeekend=(day==6))
                    ENERGY_RECIPE += e
                    RECIPE_MADE.append(r)
                    RECIPE_MADE_ENG.append(e)
                    if e>0: vitality_recovery(party)
                if ryori_eaten==2 and (time%(3600*24))>3600*18:
                    print4("-- 夜料理", end="  ")
                    # よる
                    ryori_eaten += 1
                    r, e= ryori(BAG, field, non_essential_ingrs=ing_additional, rcp_primary=rcp_primary,
                                essential_ingrs=ing_essential, n_essential_igrs=n_ing_essential,
                                isWeekend=(day==6))
                    ENERGY_RECIPE += e
                    RECIPE_MADE.append(r)
                    RECIPE_MADE_ENG.append(e)
                    if e>0: vitality_recovery(party)
                print4("-------")
                
            
            # 料理の後時間をすすめる
            time += dt
            print4(f"AFTER {dt/3600:.2f} [h] of WORK ...")
            print4("[BERRY] ", end="")
            tmp = 0
            for pk in party:
                berry, ingredients = pk.work(dt, party, field)
                print4(f"{pk.name}:+{berry:.1f}", end=", ")
                ENERGY += berry
                for ing in ingredients:
                    tmp += ing['amount']
                    if ing['kind'] in BAG:
                        BAG[ing['kind']] += ing['amount']
                    else:
                        BAG[ing['kind']] = ing['amount']
                    if ing['kind'] in TOTAL_IGR_AQUIRED:
                        TOTAL_IGR_AQUIRED[ing['kind']] += ing['amount']
                    else:
                        TOTAL_IGR_AQUIRED[ing['kind']] = ing['amount']
            else:
                print4(f"\n[INGREDIENT] +{tmp:.1f}")
            
            # 朝ならスキル発動前に元気回復
            if abs((time%(3600*24))-3600*8.5)<=1800: # 誤差30分
                for pk in party:
                    if not somebody_has_eng_bonus(party) and pk.nature["vitality"] < 0:
                        print4((pk.name, pk.vitality))
                        pk.vitality = min(88+pk.vitality, 100)
                    else:
                        pk.vitality = 105 \
                            if "eng_bonus" in pk.subskill and pk.subskill["eng_bonus"]>0 else 100
                        

            
            # スキル
            for pk in party:
                pk:Pokemon
                extra_e, extra_i, _ = pk.skill_exec(party, field)
                ENERGY += extra_e
                for ei in extra_i:
                    if ei in BAG:
                        BAG[ei] += extra_i[ei]
                    else:
                        BAG[ei] = extra_i[ei]
                    if ei in TOTAL_IGR_AQUIRED:
                        TOTAL_IGR_AQUIRED[ei] += extra_i[ei]
                    else:
                        TOTAL_IGR_AQUIRED[ei] = extra_i[ei]

            print4("[VITARITY] ", end="")
            for pk in party:
                print4(f"{pk.name}: {pk.vitality:.1f}", end=", ")
            else:
                print4("")

            # TODO ポケモン入れ替え
                

    print3("\n-----SUMMARY-----")
    for pk in party:
        pk:Pokemon
        print3(f"[{pk.name}]")
        print3(f"    総エナジー　　: {pk.cumulated_energy:.1f}")
        print3(f"    食材　　　　　: {print_dict(pk.cumulated_ingredients)}")
        print3(f"    スキル発動　　: {pk.n_skill_activated} 回")
    print3(f"\nTOTAL")    
    print3(f"    ENERGY: {ENERGY:.1f}")    
    print3(f"  RECIPE E: {ENERGY_RECIPE:.1f}")    
    print3(f"    in BAG")    
    for b in BAG:
        print3(f"    {b:<6}\t: {BAG[b]:.1f}")
    print3(f"    RECIPES MADE")
    for i, (r, e) in enumerate(zip(RECIPE_MADE, RECIPE_MADE_ENG)):
        if (i+1)%3==0:
            print3(f"{r}({e:.0f})")
        else:
            print3(f"{r}({e:.0f})", end=",")

    print3("-----------------")

    return ENERGY+ENERGY_RECIPE, TOTAL_IGR_AQUIRED, BAG, RECIPE_MADE, ENERGY_RECIPE

def somebody_has_eng_bonus(party):
    for pk in party:
        if "eng_bonus" in pk.subskill and pk.subskill["eng_bonus"]>0:
            return True
    return False

def combination_bf(pokes_must:list, pokes_other:list, n_weeks, field:Field, outfp=None, TF_skip=None, monday_setting={}, recipe_name_reserve=""):
    totaln =  math.comb(len(pokes_other), 5-len(pokes_must))
    print("Total N:",totaln)
    # TF_skipはTrue or Falseを格納する配列Trueのものだけ計算する。
    if outfp is not None:
        f = open(outfp, "a")
        f.close()
    ret = []
    for idx, party in tqdm(enumerate(itertools.combinations(pokes_other, 5-len(pokes_must)))):
        if TF_skip is not None and not TF_skip[idx]:
            # TF_skipでfalseの場合はスキップする。
            continue
        party += tuple(pokes_must)
        if outfp is not None: f = open(outfp, "a")
        # for pk in party:print2(pk.name)
        # continue
        week_energy = []
        cumu_e = 0
        cumu_e_rcp = 0
        cumu_ing = {}
        cumu_n_ing = 0
        # dryrun to determine essential ingredients
        _, ing, _, _, _ = one_week(party, field, cooks=False)
        # omit unstable ingredients
        ing_stable = {}
        for key in ing:
            if ing[key]>30:
                ing_stable[key] = ing[key]
        ing_essential, ing_additional, recipes, n_ing_essential = list_up_possible_recipe(ing_stable, field, party, recipe_name_reserve=recipe_name_reserve)
        
        # reset counters
        reset_to_Monday(party, field, **monday_setting)
        
        # start simulation
        for i in range(n_weeks):
            e, igr, bag, rcp, e_rcp = one_week(party, field, cooks=True, ing_additional=ing_additional,
                                               ing_essential=ing_essential, n_ing_essential=n_ing_essential)
            week_energy.append(e/7)
            cumu_e += e
            cumu_e_rcp += e_rcp
            for name in igr:
                cumu_n_ing += igr[name]
                if name in cumu_ing:
                    cumu_ing[name] += igr[name]
                else:
                    cumu_ing[name] = igr[name]
        # calc std error
        avg = sum(week_energy)/len(week_energy)
        variance = sum([(e-avg)**2 for e in week_energy])/len(week_energy)
        sigma = variance**0.5

        print2("--- TEST RESULT ---")
        for pk in party:
            print2(f"   * {pk.name}({pk.tribe})")
        print2(f"average energy per day: {cumu_e/n_weeks/7:.2f}")
        print2(f"average ing per day: ")
        for name in cumu_ing:
            print2(f"    {name}: {cumu_ing[name]/n_weeks/7:.2f}")
        print2(f"avg. recipe energy: {cumu_e_rcp/n_weeks/21:.1f}")

        ret.append(cumu_e/n_weeks/7)

        if outfp is not None:
            f.write(f"{field.id_recipe_request},")
            if len(recipes) < MAX_N_RECIPE_CONSIDER:
                for _ in range(MAX_N_RECIPE_CONSIDER-len(recipes)):
                    recipes.append("")
            for r in recipes:
                f.write(f"{r},")
            for pk in party:
                f.write(f"{pk.lv},")
            for pk in party:
                f.write(f"{pk.name},")
            for pk in party:
                f.write(f"{pk.cumulated_energy/n_weeks/7:.0f},")
            f.write(f"{cumu_e/n_weeks/7:.0f},{sigma:.1f},{cumu_n_ing/n_weeks/7:.1f},{cumu_e_rcp/n_weeks/21:.0f},")
            for rrr in set(rcp):
                f.write(f"{rrr},")
            f.write(f"\n")

            f.close()
    
    return ret

def print_dict(dict):
    ret = ""
    for key, val in dict.items():
        ret += f"{key}:{val:.1f}, "
    ret += ""
    return ret

def reset_to_Monday(party, field:Field, 
                    resetsPK=True,
                    monday_extra_pot_capacity=0,
                    monday_cooking_successful_rate=COOKING_SUCCESSFUL_RATE):
    field.extra_pot_capacity = monday_extra_pot_capacity
    field.cooking_successful_rate = monday_cooking_successful_rate
    if resetsPK:
        for pk in party:
            pk:Pokemon
            pk.cumulated_energy = 0
            pk.cumulated_ingredients = {}
            pk.extra_help_energy = 0
            pk.extra_help_ingredients = {}
            pk.n_skill_activated = 0

def vitality_recovery(party):
    """
    料理でポケモンの元気を回復する。
    """
    for pk in party:
        pk:Pokemon
        amount = 0
        if pk.vitality <= 20:
            amount = 5
        elif pk.vitality <= 40:
            amount = 4
        elif pk.vitality <= 60:
            amount = 3
        elif pk.vitality <= 80:
            amount = 2
        elif pk.vitality <= 150:
            amount = 1
        amount = max(amount, EVENT_BONUS_VITALITY_RECOV_AMOUNT)
        print5(f"+{amount}", end=" ")
        pk.vitality = min(150, pk.vitality + amount)
    print5("")
        
def print2(str, end=None):
    if LOG_LEVEL >= 2:print(str, end=end)
def print3(str, end=None):
    if LOG_LEVEL >= 3:print(str, end=end)
def print4(str, end=None):
    if LOG_LEVEL >= 4:print(str, end=end)
def print5(str, end=None):
    if LOG_LEVEL >= 5:print(str, end=end)

if __name__=="__main__":
    main()
