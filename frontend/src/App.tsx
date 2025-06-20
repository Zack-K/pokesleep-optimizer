import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tab,
  Tabs,
  Paper,
  Alert
} from '@mui/material';
import { styled } from '@mui/material/styles';
import PokemonList from './components/PokemonList';
import PartyOptimizer from './components/PartyOptimizer';
import SimulationResults from './components/SimulationResults';
import { Pokemon, SimulationResult } from './types';
import { pokemonApi } from './api/pokemonApi';

const StyledContainer = styled(Container)(({ theme }) => ({
  paddingTop: theme.spacing(3),
  paddingBottom: theme.spacing(3),
}));

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [pokemon, setPokemon] = useState<Pokemon[]>([]);
  const [selectedPokemon, setSelectedPokemon] = useState<string[]>([]);
  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPokemon();
  }, []);

  const loadPokemon = async () => {
    try {
      setLoading(true);
      const data = await pokemonApi.getAllPokemon();
      setPokemon(data);
    } catch (err) {
      setError('ポケモンデータの読み込みに失敗しました');
      console.error('Pokemon loading error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePokemonSelect = (pokemonNames: string[]) => {
    setSelectedPokemon(pokemonNames);
  };

  const handleSimulationComplete = (result: SimulationResult) => {
    setSimulationResult(result);
    setTabValue(2); // 結果タブに切り替え
  };

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            ポケモンスリープ 最適パーティ編成計算
          </Typography>
        </Toolbar>
      </AppBar>

      <StyledContainer maxWidth="lg">
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Paper sx={{ width: '100%' }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab label="ポケモン一覧" />
            <Tab label="パーティ最適化" />
            <Tab label="シミュレーション結果" />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            <PokemonList
              pokemon={pokemon}
              selectedPokemon={selectedPokemon}
              onPokemonSelect={handlePokemonSelect}
              loading={loading}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <PartyOptimizer
              pokemon={pokemon}
              selectedPokemon={selectedPokemon}
              onSimulationComplete={handleSimulationComplete}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <SimulationResults result={simulationResult} />
          </TabPanel>
        </Paper>
      </StyledContainer>
    </div>
  );
}

export default App;