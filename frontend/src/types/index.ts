// APIレスポンスに対応した型定義
export interface Pokemon {
  name: string;
  kind: number;
  type: string;
  frequency: number;
  berry: string;
  ingredients: string[];
  main_skill: number;
  skill_probability: number;
  ingredient_probability: number;
  inventory_size: number;
}

// UIで使用する追加プロパティを含む型
export interface PokemonWithUI extends Pokemon {
  level?: number;
  berry_energy?: number;
  selected?: boolean;
}

export interface FieldSettings {
  field_bonus: number;
  field_berry: string[];
  pot_capacity: number;
  recipe_request: number;
}

export interface SimulationResult {
  party_names: string[];
  total_energy: number;
  recipe_energy: number;
  daily_energy: number;
  ingredients: Record<string, number>;
  recipes_made: Record<string, any>;
}

export interface OptimizationRequest {
  must_include: string[];
  field_settings: FieldSettings;
  weeks_to_simulate: number;
  recipe_name_reserve: string;
}