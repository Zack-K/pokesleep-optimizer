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
  CircularProgress
} from '@mui/material';
import { Pokemon, SimulationResult, FieldSettings } from '../types';
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
      
      const request = {
        must_include: selectedPokemon,
        field_settings: fieldSettings,
        weeks_to_simulate: 3,
        recipe_name_reserve: ""
      };
      
      await pokemonApi.optimizeParty(request);
      // 最適化結果の処理を後で実装
      setError('最適化機能は開発中です');
    } catch (err) {
      setError('最適化実行中にエラーが発生しました');
      console.error('Optimization error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        パーティ最適化
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

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
                  <Typography key={name} variant="body1">
                    • {name}
                  </Typography>
                ))}
              </Box>
            )}
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
      </Grid>

      <Box mt={3} display="flex" gap={2}>
        <Button
          variant="contained"
          size="large"
          onClick={handleSimulate}
          disabled={loading || selectedPokemon.length === 0}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          シミュレーション実行
        </Button>
        
        <Button
          variant="outlined"
          size="large"
          onClick={handleOptimize}
          disabled={loading}
        >
          最適化計算
        </Button>
      </Box>
    </Box>
  );
};

export default PartyOptimizer;