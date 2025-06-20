"""
Pydanticスキーマ定義
FastAPIのベストプラクティスに従った型安全なスキーマ
"""
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from enum import Enum


class RecipeType(str, Enum):
    """レシピタイプ列挙型"""
    CURRY = "curry"
    SALAD = "salad" 
    DESSERT = "dessert"


class PokemonType(str, Enum):
    """ポケモンタイプ列挙型"""
    BERRY = "きのみ"
    INGREDIENT = "食材"
    SKILL = "スキル"
    ALL = "オール"


class PokemonNature(BaseModel):
    """ポケモンの性格"""
    freq: int = Field(0, ge=-2, le=2, description="おてつだいスピード補正")
    vitality: int = Field(0, ge=-1, le=1, description="げんき補正")
    exp: int = Field(0, ge=-1, le=1, description="けいけんち補正")
    ingr: int = Field(0, ge=-1, le=1, description="食材確率補正")
    skill: int = Field(0, ge=-1, le=1, description="スキル確率補正")


class PokemonSubSkill(BaseModel):
    """ポケモンのサブスキル"""
    skill: int = Field(0, ge=0, description="スキル確率アップ")
    speed: int = Field(0, ge=0, description="おてつだいスピードアップ")
    ingr: int = Field(0, ge=0, description="食材確率アップ")
    exp: int = Field(0, ge=0, description="けいけんちボーナス")
    help_bonus: int = Field(0, ge=0, description="おてつだいボーナス")
    berry: int = Field(0, ge=0, description="きのみの数S")
    inventory: int = Field(0, ge=0, description="最大所持数アップ")
    skill_lv_up: int = Field(0, ge=0, description="スキルレベルアップ")


class PokemonInfo(BaseModel):
    """ポケモン基本情報"""
    name: str = Field(..., min_length=1, description="ポケモン名")
    tribe: str = Field(..., min_length=1, description="種族名")
    level: int = Field(..., ge=1, le=100, description="レベル")
    berry_energy: int = Field(..., ge=1, description="きのみエナジー")
    main_skill: int = Field(..., ge=1, description="メインスキルID")
    ingredients: List[str] = Field(..., min_items=1, max_items=3, description="食材リスト")
    skill_probability: float = Field(..., ge=0.0, le=1.0, description="スキル発動確率")


class FieldSettings(BaseModel):
    """フィールド設定"""
    field_bonus: float = Field(1.57, ge=1.0, le=2.0, description="フィールドボーナス")
    field_berry: List[str] = Field(default_factory=list, description="フィールドのきのみ")
    pot_capacity: int = Field(69, ge=10, le=200, description="鍋容量")
    recipe_request: int = Field(1, ge=1, le=3, description="レシピタイプ")

    @validator('field_bonus')
    def validate_field_bonus(cls, v):
        if not (1.0 <= v <= 2.0):
            raise ValueError('フィールドボーナスは1.0から2.0の範囲で指定してください')
        return v


class OptimizationRequest(BaseModel):
    """最適化リクエスト"""
    must_include: List[str] = Field(default_factory=list, description="必須ポケモン")
    field_settings: FieldSettings = Field(default_factory=FieldSettings, description="フィールド設定")
    weeks_to_simulate: int = Field(3, ge=1, le=10, description="シミュレーション週数")
    recipe_name_reserve: str = Field("", description="予約レシピ名")

    @validator('must_include')
    def validate_must_include(cls, v):
        if len(v) > 5:
            raise ValueError('必須ポケモンは最大5匹まで指定可能です')
        return v


class SimulationResult(BaseModel):
    """シミュレーション結果"""
    party_names: List[str] = Field(..., min_items=5, max_items=5, description="パーティメンバー")
    total_energy: float = Field(..., ge=0, description="総エナジー")
    recipe_energy: float = Field(..., ge=0, description="レシピエナジー")
    daily_energy: float = Field(..., ge=0, description="1日平均エナジー")
    ingredients: Dict[str, float] = Field(..., description="獲得食材")
    recipes_made: List[str] = Field(..., description="作成レシピリスト")


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    error: str = Field(..., description="エラータイプ")
    message: str = Field(..., description="エラーメッセージ")
    details: Optional[Dict] = Field(None, description="詳細情報")


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str = Field(..., description="ステータス")
    pokemon_count: int = Field(..., ge=0, description="読み込み済みポケモン数")
    version: str = Field(..., description="APIバージョン")