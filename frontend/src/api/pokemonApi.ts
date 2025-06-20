import axios from 'axios';
import { Pokemon, SimulationResult, FieldSettings, OptimizationRequest } from '../types';

// 環境に応じたAPI Base URLの決定
const getApiBaseUrl = (): string => {
  // 明示的に環境変数が設定されている場合はそれを使用
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // 開発環境のデフォルト設定
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

// デバッグ用：環境変数とAPIベースURLをログ出力
console.log('Environment:', {
  NODE_ENV: process.env.NODE_ENV,
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  API_BASE_URL: API_BASE_URL,
  location: window.location.origin
});

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10秒のタイムアウト
});

export const pokemonApi = {
  // 全ポケモン取得
  async getAllPokemon(): Promise<Pokemon[]> {
    const response = await api.get('/api/v1/pokemon/');
    return response.data;
  },

  // ポケモン名一覧取得
  async getPokemonNames(): Promise<string[]> {
    const response = await api.get('/api/v1/pokemon/names');
    return response.data;
  },

  // 特定ポケモン取得
  async getPokemon(name: string): Promise<Pokemon> {
    const response = await api.get(`/api/v1/pokemon/${encodeURIComponent(name)}`);
    return response.data;
  },

  // タイプ別ポケモン取得
  async getPokemonByType(type: string): Promise<string[]> {
    const response = await api.get(`/api/v1/pokemon/type/${encodeURIComponent(type)}`);
    return response.data;
  },

  // パーティ構成検証
  async validateParty(partyNames: string[]): Promise<any> {
    const response = await api.post('/api/v1/pokemon/validate-party', partyNames);
    return response.data;
  },

  // パーティ評価
  async evaluateParty(
    partyNames: string[],
    fieldBonus: number = 1.57,
    potCapacity: number = 69,
    weeksToSimulate: number = 3
  ): Promise<any> {
    const response = await api.post('/api/v1/pokemon/evaluate', partyNames, {
      params: {
        field_bonus: fieldBonus,
        pot_capacity: potCapacity,
        weeks_to_simulate: weeksToSimulate,
      },
    });
    return response.data;
  },

  // パーティ最適化実行
  async optimizeParty(request: OptimizationRequest): Promise<any> {
    const response = await api.post('/api/v1/pokemon/optimize', request);
    return response.data;
  },

  // Pokemon APIヘルスチェック
  async pokemonHealthCheck(): Promise<{ status: string; pokemon_count: number; version: string }> {
    const response = await api.get('/api/v1/pokemon/health');
    return response.data;
  },

  // アプリケーション全体のヘルスチェック
  async healthCheck(): Promise<{ status: string; pokemon_loaded: number; version: string }> {
    const response = await api.get('/health');
    return response.data;
  },
};

// リクエストインターセプター
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`
    });
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// エラーインターセプター
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      url: response.config.url,
      dataLength: JSON.stringify(response.data).length
    });
    return response;
  },
  (error) => {
    console.error('API Error:', {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      baseURL: error.config?.baseURL
    });
    throw error;
  }
);