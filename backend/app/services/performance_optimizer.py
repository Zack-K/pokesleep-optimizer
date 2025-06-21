"""
パフォーマンス最適化サービス
並列処理、キャッシュ、ベンチマーク機能
"""
import time
import json
import hashlib
import asyncio
import logging
import threading
import psutil
from typing import List, Dict, Any, Callable, Optional, Union
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import OrderedDict
from dataclasses import dataclass, field
from .simulation_service import optimization_service

logger = logging.getLogger(__name__)


class ParallelOptimizer:
    """並列処理最適化クラス"""
    
    def __init__(self, evaluation_function: Callable, max_workers: Optional[int] = None,
                 executor_type: str = "thread"):
        """
        並列処理最適化器の初期化
        
        Args:
            evaluation_function: 評価関数
            max_workers: 最大ワーカー数
            executor_type: エグゼキューター種類 ("thread", "process", "async")
        """
        self.evaluation_function = evaluation_function
        self.max_workers = max_workers or min(32, (psutil.cpu_count() or 1) + 4)
        self.executor_type = executor_type
    
    def evaluate_parties_parallel(self, parties: List[List[str]]) -> List[float]:
        """パーティリストを並列評価"""
        if self.executor_type == "thread":
            return self._evaluate_with_threads(parties)
        elif self.executor_type == "process":
            return self._evaluate_with_processes(parties)
        else:
            raise ValueError(f"未対応のエグゼキューター種類: {self.executor_type}")
    
    async def evaluate_parties_async(self, parties: List[List[str]]) -> List[float]:
        """パーティリストを非同期評価"""
        tasks = []
        for party in parties:
            task = asyncio.create_task(self.evaluation_function(party))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    def _evaluate_with_threads(self, parties: List[List[str]]) -> List[float]:
        """スレッドプールで並列評価"""
        results = [0.0] * len(parties)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Future辞書でインデックスを保持
            future_to_index = {
                executor.submit(self.evaluation_function, party): i 
                for i, party in enumerate(parties)
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                except Exception as e:
                    logger.error(f"パーティ評価エラー (index {index}): {e}")
                    results[index] = 0.0
        
        return results
    
    def _evaluate_with_processes(self, parties: List[List[str]]) -> List[float]:
        """プロセスプールで並列評価"""
        results = [0.0] * len(parties)
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(self.evaluation_function, party): i 
                for i, party in enumerate(parties)
            }
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                except Exception as e:
                    logger.error(f"パーティ評価エラー (index {index}): {e}")
                    results[index] = 0.0
        
        return results


class CacheManager:
    """キャッシュ管理クラス"""
    
    def __init__(self, max_size: int = 1000):
        """
        キャッシュ管理器の初期化
        
        Args:
            max_size: 最大キャッシュサイズ
        """
        self.max_size = max_size
        self.data: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """キャッシュから値を取得"""
        with self._lock:
            if key in self.data:
                # LRU: アクセスされた項目を最後に移動
                value = self.data.pop(key)
                self.data[key] = value
                self.hits += 1
                return value
            else:
                self.misses += 1
                return None
    
    def set(self, key: str, value: Any):
        """キャッシュに値を設定"""
        with self._lock:
            if key in self.data:
                # 既存キーの更新
                self.data.pop(key)
            elif len(self.data) >= self.max_size:
                # LRU: 最も古い項目を削除
                self.data.popitem(last=False)
            
            self.data[key] = value
    
    def clear(self):
        """キャッシュをクリア"""
        with self._lock:
            self.data.clear()
            self.hits = 0
            self.misses = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """キャッシュ統計を取得"""
        total_accesses = self.hits + self.misses
        hit_rate = self.hits / total_accesses if total_accesses > 0 else 0.0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.data),
            "max_size": self.max_size
        }
    
    def _generate_hash(self, party: List[str], settings: Dict[str, Any]) -> str:
        """パーティと設定からハッシュキーを生成"""
        # パーティをソートして順序を統一
        sorted_party = sorted(party)
        
        # 設定も含めてハッシュ化
        hash_data = {
            "party": sorted_party,
            "settings": sorted(settings.items())
        }
        
        hash_string = json.dumps(hash_data, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()


class OptimizationCache:
    """最適化専用キャッシュクラス"""
    
    def __init__(self, enable_cache: bool = True, max_cache_size: int = 1000,
                 cache_file: Optional[str] = None):
        """
        最適化キャッシュの初期化
        
        Args:
            enable_cache: キャッシュ有効化フラグ
            max_cache_size: 最大キャッシュサイズ
            cache_file: キャッシュファイルパス
        """
        self.enable_cache = enable_cache
        self.cache = CacheManager(max_cache_size) if enable_cache else None
        self.cache_file = cache_file
        
        if cache_file and enable_cache:
            self.load_cache()
    
    def evaluate_party(self, party: List[str], **kwargs) -> Dict[str, Any]:
        """キャッシュ機能付きパーティ評価"""
        if not self.enable_cache:
            return self._direct_evaluation(party, **kwargs)
        
        # キャッシュキーの生成
        cache_key = self.cache._generate_hash(party, kwargs)
        
        # キャッシュから検索
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"キャッシュヒット: {party}")
            return cached_result
        
        # キャッシュミス: 直接評価
        result = self._direct_evaluation(party, **kwargs)
        
        # 結果をキャッシュに保存
        self.cache.set(cache_key, result)
        logger.debug(f"キャッシュ保存: {party}")
        
        return result
    
    def _direct_evaluation(self, party: List[str], **kwargs) -> Dict[str, Any]:
        """直接評価実行"""
        return optimization_service.evaluate_specific_party(
            party_names=party,
            field_bonus=kwargs.get("field_bonus", 1.57),
            pot_capacity=kwargs.get("pot_capacity", 69),
            recipe_requests=kwargs.get("recipe_requests", ["カレー"]),
            weeks_to_simulate=kwargs.get("weeks_to_simulate", 3)
        )
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """キャッシュ統計を取得"""
        if not self.enable_cache:
            return {"cache_enabled": False}
        
        stats = self.cache.get_statistics()
        stats["cache_enabled"] = True
        return stats
    
    def clear_cache(self):
        """キャッシュをクリア"""
        if self.enable_cache:
            self.cache.clear()
    
    def save_cache(self):
        """キャッシュをファイルに保存"""
        if not self.enable_cache or not self.cache_file:
            return
        
        try:
            cache_data = {
                "data": dict(self.cache.data),
                "stats": self.cache.get_statistics()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"キャッシュ保存完了: {self.cache_file}")
        except Exception as e:
            logger.error(f"キャッシュ保存エラー: {e}")
    
    def load_cache(self):
        """ファイルからキャッシュをロード"""
        if not self.enable_cache or not self.cache_file:
            return
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # キャッシュデータを復元
            for key, value in cache_data.get("data", {}).items():
                self.cache.set(key, value)
            
            logger.info(f"キャッシュロード完了: {self.cache_file}")
        except FileNotFoundError:
            logger.info(f"キャッシュファイルが見つかりません: {self.cache_file}")
        except Exception as e:
            logger.error(f"キャッシュロードエラー: {e}")


class BenchmarkRunner:
    """ベンチマークランナークラス"""
    
    def __init__(self):
        """ベンチマークランナーの初期化"""
        pass
    
    def run_optimization_benchmark(
        self, 
        optimizer_function: Callable,
        methods: List[str],
        test_params: Dict[str, Any] = None,
        runs_per_method: int = 3
    ) -> List[Dict[str, Any]]:
        """最適化手法のベンチマーク実行"""
        if test_params is None:
            test_params = {}
        
        all_results = []
        
        for method in methods:
            method_results = []
            
            for run in range(runs_per_method):
                logger.info(f"ベンチマーク実行: {method}, run {run + 1}/{runs_per_method}")
                
                start_time = time.time()
                try:
                    result = optimizer_function(method=method, **test_params)
                    execution_time = time.time() - start_time
                    
                    benchmark_result = {
                        "method": method,
                        "run": run + 1,
                        "execution_time": execution_time,
                        "success": True,
                        **result
                    }
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    benchmark_result = {
                        "method": method,
                        "run": run + 1,
                        "execution_time": execution_time,
                        "success": False,
                        "error": str(e)
                    }
                    logger.error(f"ベンチマークエラー ({method}, run {run + 1}): {e}")
                
                method_results.append(benchmark_result)
                all_results.append(benchmark_result)
        
        return all_results
    
    def measure_execution_time(self, function: Callable, *args, **kwargs) -> float:
        """関数の実行時間を測定"""
        start_time = time.time()
        try:
            result = function(*args, **kwargs)
            return time.time() - start_time
        except Exception as e:
            logger.error(f"実行時間測定エラー: {e}")
            return time.time() - start_time
    
    def generate_performance_report(self, benchmark_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """パフォーマンスレポートを生成"""
        method_stats = {}
        
        # 手法ごとに統計を計算
        for result in benchmark_results:
            method = result["method"]
            if method not in method_stats:
                method_stats[method] = {
                    "execution_times": [],
                    "success_count": 0,
                    "total_runs": 0
                }
            
            method_stats[method]["execution_times"].append(result["execution_time"])
            method_stats[method]["total_runs"] += 1
            if result.get("success", False):
                method_stats[method]["success_count"] += 1
        
        # 統計値を計算
        report = {}
        min_avg_time = float('inf')
        
        for method, stats in method_stats.items():
            times = stats["execution_times"]
            avg_time = sum(times) / len(times)
            min_avg_time = min(min_avg_time, avg_time)
            
            report[method] = {
                "average_execution_time": avg_time,
                "min_execution_time": min(times),
                "max_execution_time": max(times),
                "success_rate": stats["success_count"] / stats["total_runs"],
                "total_runs": stats["total_runs"]
            }
        
        # 相対速度を計算
        for method_report in report.values():
            method_report["relative_speed"] = min_avg_time / method_report["average_execution_time"]
        
        return report


class MemoryProfiler:
    """メモリプロファイラークラス"""
    
    def __init__(self):
        """メモリプロファイラーの初期化"""
        self.process = psutil.Process()
        self.monitoring = False
        self.start_memory = 0
        self.peak_memory = 0
    
    def start_monitoring(self):
        """メモリ監視開始"""
        self.monitoring = True
        self.start_memory = self.get_current_memory_usage()
        self.peak_memory = self.start_memory
        logger.info(f"メモリ監視開始: {self.start_memory:.2f}MB")
    
    def stop_monitoring(self) -> Dict[str, float]:
        """メモリ監視終了"""
        if not self.monitoring:
            raise RuntimeError("メモリ監視が開始されていません")
        
        current_memory = self.get_current_memory_usage()
        self.monitoring = False
        
        memory_info = {
            "start_memory_mb": self.start_memory,
            "current_memory_mb": current_memory,
            "peak_memory_mb": self.peak_memory,
            "memory_increase_mb": current_memory - self.start_memory
        }
        
        logger.info(f"メモリ監視終了: ピーク{self.peak_memory:.2f}MB, 増加{memory_info['memory_increase_mb']:.2f}MB")
        return memory_info
    
    def get_current_memory_usage(self) -> float:
        """現在のメモリ使用量を取得（MB）"""
        try:
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024  # バイトからMBに変換
            
            if self.monitoring:
                self.peak_memory = max(self.peak_memory, memory_mb)
            
            return memory_mb
        except Exception as e:
            logger.error(f"メモリ使用量取得エラー: {e}")
            return 0.0
    
    def detect_memory_leaks(self, baseline_memory: float, 
                          current_memory: float, threshold_mb: float = 50.0) -> Dict[str, Any]:
        """メモリリークを検出"""
        memory_increase = current_memory - baseline_memory
        potential_leak = memory_increase > threshold_mb
        
        leak_report = {
            "baseline_memory_mb": baseline_memory,
            "current_memory_mb": current_memory,
            "memory_increase_mb": memory_increase,
            "threshold_mb": threshold_mb,
            "potential_leak": potential_leak
        }
        
        if potential_leak:
            logger.warning(f"メモリリーク検出: {memory_increase:.2f}MB増加")
        
        return leak_report
    
    def get_system_memory_info(self) -> Dict[str, Any]:
        """システムメモリ情報を取得"""
        try:
            virtual_memory = psutil.virtual_memory()
            return {
                "total_memory_gb": virtual_memory.total / 1024 / 1024 / 1024,
                "available_memory_gb": virtual_memory.available / 1024 / 1024 / 1024,
                "memory_usage_percent": virtual_memory.percent,
                "cpu_count": psutil.cpu_count()
            }
        except Exception as e:
            logger.error(f"システムメモリ情報取得エラー: {e}")
            return {}