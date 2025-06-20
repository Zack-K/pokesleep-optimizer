"""
ポケモンのモデル定義
循環インポートを避けるため、Pokemonクラスを独立したファイルに分離
"""
import math
import random
from typing import List, Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from scipy.special import comb
from scipy.stats import binom

# define.pyからの必要な定数をここでインポート
from define import *

class Pokemon:
    def __init__(self, name, tribe, lv,
                 ingredients: list,
                 vitality, nature={"freq":0, "vitality":0, "exp":0, "ingr":0, "skill":0}, 
                 subskill={"skill":0, "speed":0, "ingr":0, "exp":0, "help_bonus":0, "berry":0, "inventory":0},
                 mainskill_lv=1,
                 n_evolve=0):
        self.name = name
        self.lv = max(lv, FORCE_PK_LV) if FORCE_PK_LV is not None else lv
        self.tribe = tribe
        self.pokemon = POKEMON[tribe]
        self.nature = nature
        self.subskill = {}
        
        # サブスキルの処理
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
        
        # メインスキルレベルの設定
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
        slvadd = self.subskill.get("skill_lv_up", 0)
        slvadd += EVENT_BONUS_SKILL_LV_UP['amount'] \
                if self.pokemon['kind'] in EVENT_BONUS_SKILL_LV_UP['kind'] \
                or self.pokemon['type'] in EVENT_BONUS_SKILL_LV_UP['type'] \
                else 0
        self.mainskill_lv = min(mainskill_lv + slvadd, slvmax)
        
        # きのみエナジーの計算
        self.berry_energy = round(max(BERRY[self.pokemon["berry"]]+self.lv-1, BERRY[self.pokemon["berry"]]*1.025**(self.lv-1)))
        
        # 性格の処理
        nature["freq"] = nature["freq"] if 0 < nature["freq"] else 0.75 * nature["freq"]
        self.base_freq = self.pokemon["freq"]*(1-(self.lv-1)*0.002)*(1-0.1*nature["freq"])
        self.ss_faster = self.subskill["speed"] * 0.07
        
        # 食材の設定
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
        
        self.n_evolve = n_evolve
        self.skill_standby = 0
        
        # きのみ数の設定
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
        
        # スキル確率の計算
        fact = EVENT_BONUS_SKILL_TRIGGER['fact'] \
                if self.pokemon['kind'] in EVENT_BONUS_SKILL_TRIGGER['kind'] \
                or self.pokemon['type'] in EVENT_BONUS_SKILL_TRIGGER['type'] \
                else 1
        self.skill_prob = PROBABILITY[tribe]['skill']/100 * (1 + 0.18*self.subskill['skill']) * (1+0.2*nature["skill"]) * fact
        self.ingr_prob = PROBABILITY[tribe]['ingr']/100 * (1 + 0.18*self.subskill['ingr']) * (1+0.2*nature["ingr"])
        
        # インベントリの設定
        if "inventory" in self.subskill:
            self.inventory = INVENTORY[tribe] + 6*self.subskill['inventory'] + 5*self.n_evolve
        else:
            self.inventory = INVENTORY[tribe] + 5*self.n_evolve
        if GCT:
            self.inventory = round(self.inventory*1.5)

        # 統計用変数の初期化
        self.n_skill_activated = 0
        self.cumulated_energy = 0
        self.cumulated_ingredients = {}
        self.misfire_counter = 0
        self.extra_help_energy = 0
        self.extra_help_ingredients = {}
        
        # 回復係数
        if self.nature["vitality"] < 0:
            self.recov_fact = 0.88
        elif self.nature["vitality"] > 0:
            self.recov_fact = 1.2
        else:
            self.recov_fact = 1.0
        
        # 1回のお手伝いでのアイテム数
        if self.lv >= 60:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + sum(self.n_ingr) * self.ingr_prob / 3
        elif self.lv >= 30:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + sum(self.n_ingr[0:2]) * self.ingr_prob / 2
        else:
            self.n_item_single_help = self.n_berry * (1 - self.ingr_prob) + self.n_ingr[0] * self.ingr_prob 

    def show_ability(self):
        """ポケモンの能力を表示"""
        print(f"{self.name}({self.tribe})")
        m = (self.base_freq*(1-self.ss_faster))//60
        s = (self.base_freq*(1-self.ss_faster))-60*m
        print(f"            freq: {m:.0f}:{s:.0f}")
        if GCT:
            m = (self.base_freq*(1-self.ss_faster)/1.2)//60
            s = (self.base_freq*(1-self.ss_faster)/1.2)-60*m
            print(f"        GCT freq: {m:.0f}:{s:.0f}")
        print(f"    berry energy: {self.berry_energy}")
        print(f"        skill lv: {self.mainskill_lv}")
        print(f"           skill: {self.skill_prob*100:.1f}%")
        print(f"     ingredients: {self.ingredients}")
        print(f"   n ingredients: {self.n_ingr}")
        print(f" ingredient prob: {self.ingr_prob*100:.1f}%")
        print(f"       inventory: {self.inventory}")
        print(f" N item / a help: {self.n_item_single_help}")

    # 他のメソッドは元のコードから移植
    def recovery(self, vitality):
        self.vitality += vitality
    
    def skill_activate_probability(self, n_help):
        return 1 - (1-self.skill_prob)**n_help

    def skill_activate_probability_n_times(self, n_activation, n_help):
        return comb(n_help, n_activation)*\
                    self.skill_prob**n_activation*\
                    (1-self.skill_prob)**(n_help-n_activation)
    
    def skill_activate_probability_two_times(self, n_help):
        return self.skill_activate_probability(n_help) - self.skill_activate_probability_n_times(1, n_help)

    def skill_activate_probability_above_n_times(self, n_activation, n_help):
        n_help = round(n_help)
        probability = 1 - binom.cdf(n_activation-1, n_help, self.skill_prob)
        return probability