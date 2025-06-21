import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Grid,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Tabs,
  Tab,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import { Pokemon, SimulationResult, FieldSettings, OptimizationRequest } from '../types';
import { pokemonApi } from '../api/pokemonApi';

interface PartyOptimizerProps {
  pokemon: Pokemon[];
  selectedPokemon: string[];
  onSimulationComplete: (result: SimulationResult) => void;
}

const PartyOptimizer: React.FC<PartyOptimizerProps> = ({
  pokemon,
  selectedPokemon,
  onSimulationComplete
}) => {
  const [fieldSettings, setFieldSettings] = useState<FieldSettings>({
    field_bonus: 1.57,
    field_berry: [],
    pot_capacity: 69,
    recipe_request: 1 // ID_RECIPE_CURRY
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // 新しい最適化機能用の状態
  const [selectedTab, setSelectedTab] = useState(0);
  const [optimizationMethod, setOptimizationMethod] = useState<'brute_force' | 'genetic' | 'multi_objective'>('genetic');
  const [multiObjectiveType, setMultiObjectiveType] = useState<'balanced' | 'energy_focused' | 'recipe_focused'>('balanced');
  const [optimizationResults, setOptimizationResults] = useState<any>(null);
  const [benchmarkResults, setBenchmarkResults] = useState<any>(null);
  const [optimizationProgress, setOptimizationProgress] = useState<number>(0);

  const handleSimulate = async () => {
    if (selectedPokemon.length === 0) {
      setError('最低1匹のポケモンを選択してください');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const result = await pokemonApi.evaluateParty(
        selectedPokemon,
        fieldSettings.field_bonus,
        fieldSettings.pot_capacity,
        3 // 3週間のシミュレーション
      );
      onSimulationComplete(result);
    } catch (err) {
      setError('シミュレーション実行中にエラーが発生しました');
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async () => {
    try {
      setLoading(true);
      setError(null);
      setOptimizationProgress(0);
      
      const request: OptimizationRequest = {
        must_include: selectedPokemon,
        field_settings: fieldSettings,
        weeks_to_simulate: 3,
        recipe_name_reserve: ""
      };
      
      let result;
      
      if (optimizationMethod === 'genetic') {
        setOptimizationProgress(25);
        result = await pokemonApi.optimizePartyGenetic(request);
        setOptimizationProgress(100);
      } else if (optimizationMethod === 'multi_objective') {
        setOptimizationProgress(25);
        result = await pokemonApi.optimizePartyMultiObjective(request, multiObjectiveType);
        setOptimizationProgress(100);
      } else {
        setOptimizationProgress(25);
        result = await pokemonApi.optimizeParty(request);
        setOptimizationProgress(100);
      }
      
      setOptimizationResults(result);
      
      // シミュレーション結果を親コンポーネントに通知
      onSimulationComplete({
        party_names: result.party_names,
        total_energy: result.total_energy || result.fitness,
        daily_energy: result.daily_energy,
        recipe_energy: result.recipe_energy || 0,
        ingredients: result.ingredients || {},
        recipes_made: result.recipes_made || {}
      });
      
    } catch (err) {
      setError('最適化実行中にエラーが発生しました');
      console.error('Optimization error:', err);
    } finally {
      setLoading(false);
      setOptimizationProgress(0);
    }
  };

  const handleBenchmark = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const request: OptimizationRequest = {
        must_include: selectedPokemon,
        field_settings: fieldSettings,
        weeks_to_simulate: 3,
        recipe_name_reserve: ""
      };
      
      const result = await pokemonApi.benchmarkOptimization(
        request,
        ['brute_force', 'genetic', 'multi_objective'],
        2 // 各手法2回実行
      );
      
      setBenchmarkResults(result);
      
    } catch (err) {
      setError('ベンチマーク実行中にエラーが発生しました');
      console.error('Benchmark error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        パーティ最適化
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Tabs value={selectedTab} onChange={(_, newValue) => setSelectedTab(newValue)} sx={{ mb: 3 }}>
        <Tab label="最適化実行" />
        <Tab label="結果表示" />
        <Tab label="ベンチマーク" />
      </Tabs>

      {/* 最適化実行タブ */}
      {selectedTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                選択中のパーティ ({selectedPokemon.length}/5)
              </Typography>
              {selectedPokemon.length === 0 ? (
                <Typography color="textSecondary">
                  ポケモン一覧タブでポケモンを選択してください
                </Typography>
              ) : (
                <Box>
                  {selectedPokemon.map((name) => (
                    <Chip key={name} label={name} sx={{ m: 0.5 }} />
                  ))}
                </Box>
              )}
            </Paper>

            <Paper sx={{ p: 3, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                最適化手法選択
              </Typography>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>最適化アルゴリズム</InputLabel>
                <Select
                  value={optimizationMethod}
                  label="最適化アルゴリズム"
                  onChange={(e) => setOptimizationMethod(e.target.value as any)}
                >
                  <MenuItem value="brute_force">総当たり</MenuItem>
                  <MenuItem value="genetic">遺伝的アルゴリズム</MenuItem>
                  <MenuItem value="multi_objective">マルチ目的最適化</MenuItem>
                </Select>
              </FormControl>

              {optimizationMethod === 'multi_objective' && (
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>最適化目的</InputLabel>
                  <Select
                    value={multiObjectiveType}
                    label="最適化目的"
                    onChange={(e) => setMultiObjectiveType(e.target.value as any)}
                  >
                    <MenuItem value="balanced">バランス重視</MenuItem>
                    <MenuItem value="energy_focused">エナジー重視</MenuItem>
                    <MenuItem value="recipe_focused">レシピ重視</MenuItem>
                  </Select>
                </FormControl>
              )}

              <Typography variant="body2" color="textSecondary">
                {optimizationMethod === 'brute_force' && '総当たり: 全ての組み合わせを評価（時間がかかります）'}
                {optimizationMethod === 'genetic' && '遺伝的アルゴリズム: 効率的な探索で高品質な解を発見'}
                {optimizationMethod === 'multi_objective' && 'マルチ目的最適化: 複数の目標を同時に最適化'}
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                フィールド設定
              </Typography>
              
              <Box mb={3}>
                <Typography gutterBottom>フィールドボーナス: {fieldSettings.field_bonus}</Typography>
                <Slider
                  value={fieldSettings.field_bonus}
                  onChange={(_, value) => setFieldSettings(prev => ({
                    ...prev,
                    field_bonus: value as number
                  }))}
                  min={1.0}
                  max={2.0}
                  step={0.01}
                  marks={[
                    { value: 1.0, label: '1.0' },
                    { value: 1.57, label: '1.57' },
                    { value: 2.0, label: '2.0' }
                  ]}
                />
              </Box>

              <Box mb={3}>
                <TextField
                  fullWidth
                  label="鍋容量"
                  type="number"
                  value={fieldSettings.pot_capacity}
                  onChange={(e) => setFieldSettings(prev => ({
                    ...prev,
                    pot_capacity: parseInt(e.target.value) || 69
                  }))}
                />
              </Box>

              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>レシピ種類</InputLabel>
                <Select
                  value={fieldSettings.recipe_request}
                  label="レシピ種類"
                  onChange={(e) => setFieldSettings(prev => ({
                    ...prev,
                    recipe_request: e.target.value as number
                  }))}
                >
                  <MenuItem value={1}>カレー</MenuItem>
                  <MenuItem value={2}>サラダ</MenuItem>
                  <MenuItem value={3}>デザート</MenuItem>
                </Select>
              </FormControl>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            {loading && optimizationProgress > 0 && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" gutterBottom>
                  最適化実行中... {optimizationProgress}%
                </Typography>
                <LinearProgress variant="determinate" value={optimizationProgress} />
              </Box>
            )}

            <Box display="flex" gap={2}>
              <Button
                variant="contained"
                size="large"
                onClick={handleSimulate}
                disabled={loading || selectedPokemon.length === 0}
                startIcon={loading && selectedTab === 0 ? <CircularProgress size={20} /> : null}
              >
                シミュレーション実行
              </Button>
              
              <Button
                variant="contained"
                color="primary"
                size="large"
                onClick={handleOptimize}
                disabled={loading}
                startIcon={loading && selectedTab === 0 ? <CircularProgress size={20} /> : null}
              >
                最適化実行
              </Button>

              <Button
                variant="outlined"
                size="large"
                onClick={handleBenchmark}
                disabled={loading}
              >
                ベンチマーク実行
              </Button>
            </Box>
          </Grid>
        </Grid>
      )}

      {/* 結果表示タブ */}
      {selectedTab === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            {optimizationResults ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    最適化結果 ({optimizationResults.optimization_method || '不明'})
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" gutterBottom>
                        最適パーティ
                      </Typography>
                      <Box>
                        {(optimizationResults.party_names || []).map((name: string) => (
                          <Chip key={name} label={name} sx={{ m: 0.5 }} color="primary" />
                        ))}
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" gutterBottom>
                        パフォーマンス指標
                      </Typography>
                      <Typography>総エナジー: {(optimizationResults.total_energy || optimizationResults.fitness || 0).toLocaleString()}</Typography>
                      <Typography>日平均エナジー: {(optimizationResults.daily_energy || 0).toLocaleString()}</Typography>
                      {optimizationResults.generations_completed && (
                        <Typography>完了世代数: {optimizationResults.generations_completed}</Typography>
                      )}
                    </Grid>

                    {optimizationResults.objectives && (
                      <Grid item xs={12}>
                        <Typography variant="subtitle1" gutterBottom>
                          目的関数値
                        </Typography>
                        <Box>
                          {optimizationResults.objective_names?.map((name: string, index: number) => (
                            <Chip 
                              key={name} 
                              label={`${name}: ${optimizationResults.objectives[index]?.toFixed(2)}`}
                              sx={{ m: 0.5 }}
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      </Grid>
                    )}

                    {/* 食材情報表示 */}
                    {optimizationResults.ingredients && Object.keys(optimizationResults.ingredients).length > 0 && (
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                          獲得食材
                        </Typography>
                        <Box>
                          {Object.entries(optimizationResults.ingredients).map(([ingredient, amount]: [string, any]) => (
                            <Typography key={ingredient} variant="body2">
                              {ingredient}: {amount}
                            </Typography>
                          ))}
                        </Box>
                      </Grid>
                    )}

                    {/* レシピ情報表示 */}
                    {optimizationResults.recipes_made && Object.keys(optimizationResults.recipes_made).length > 0 && (
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                          作成レシピ
                        </Typography>
                        <Box>
                          {Object.entries(optimizationResults.recipes_made).map(([recipe, data]: [string, any]) => (
                            <Typography key={recipe} variant="body2">
                              {recipe}: {data.count || 0}回 (エナジー: {data.energy || 0})
                            </Typography>
                          ))}
                        </Box>
                      </Grid>
                    )}

                    {optimizationResults.pareto_front && (
                      <Grid item xs={12}>
                        <Typography variant="subtitle1" gutterBottom>
                          パレート最適解 ({optimizationResults.pareto_front.length}個)
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          複数の目標間でトレードオフが存在する解集合
                        </Typography>
                      </Grid>
                    )}
                  </Grid>
                </CardContent>
              </Card>
            ) : (
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="body1" color="textSecondary">
                  最適化を実行すると結果がここに表示されます
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      )}

      {/* ベンチマークタブ */}
      {selectedTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            {benchmarkResults ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    ベンチマーク結果
                  </Typography>
                  
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>最適化手法</TableCell>
                          <TableCell align="right">平均実行時間 (秒)</TableCell>
                          <TableCell align="right">相対速度</TableCell>
                          <TableCell align="right">成功率</TableCell>
                          <TableCell align="right">実行回数</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {Object.entries(benchmarkResults.performance_report || {}).map(([method, stats]: [string, any]) => (
                          <TableRow key={method}>
                            <TableCell component="th" scope="row">
                              {method === 'brute_force' ? '総当たり' : 
                               method === 'genetic' ? '遺伝的アルゴリズム' : 
                               method === 'multi_objective' ? 'マルチ目的最適化' : method}
                            </TableCell>
                            <TableCell align="right">{stats.average_execution_time?.toFixed(2)}</TableCell>
                            <TableCell align="right">{stats.relative_speed?.toFixed(2)}x</TableCell>
                            <TableCell align="right">{(stats.success_rate * 100)?.toFixed(1)}%</TableCell>
                            <TableCell align="right">{stats.total_runs}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            ) : (
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="body1" color="textSecondary">
                  ベンチマークを実行すると結果がここに表示されます
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default PartyOptimizer;