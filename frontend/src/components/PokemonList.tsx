import React, { useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Checkbox,
  TextField,
  Box,
  Chip,
  CircularProgress,
  FormControlLabel
} from '@mui/material';
import { Pokemon } from '../types';

interface PokemonListProps {
  pokemon: Pokemon[];
  selectedPokemon: string[];
  onPokemonSelect: (pokemonNames: string[]) => void;
  loading: boolean;
}

const PokemonList: React.FC<PokemonListProps> = ({
  pokemon,
  selectedPokemon,
  onPokemonSelect,
  loading
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showSelectedOnly, setShowSelectedOnly] = useState(false);

  const filteredPokemon = pokemon.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         p.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = !showSelectedOnly || selectedPokemon.includes(p.name);
    return matchesSearch && matchesFilter;
  });

  const handlePokemonToggle = (pokemonName: string) => {
    const currentIndex = selectedPokemon.indexOf(pokemonName);
    const newSelected = [...selectedPokemon];

    if (currentIndex === -1) {
      if (newSelected.length < 5) {
        newSelected.push(pokemonName);
      }
    } else {
      newSelected.splice(currentIndex, 1);
    }

    onPokemonSelect(newSelected);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box mb={3}>
        <TextField
          fullWidth
          label="ポケモン検索"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ mb: 2 }}
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={showSelectedOnly}
              onChange={(e) => setShowSelectedOnly(e.target.checked)}
            />
          }
          label="選択済みのみ表示"
        />
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          選択済み: {selectedPokemon.length}/5匹
        </Typography>
      </Box>

      <Grid container spacing={2}>
        {filteredPokemon.map((p) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={p.name}>
            <Card
              sx={{
                cursor: 'pointer',
                border: selectedPokemon.includes(p.name) ? 2 : 1,
                borderColor: selectedPokemon.includes(p.name) ? 'primary.main' : 'grey.300',
                '&:hover': {
                  boxShadow: 3,
                },
              }}
              onClick={() => handlePokemonToggle(p.name)}
            >
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  <Checkbox
                    checked={selectedPokemon.includes(p.name)}
                    onChange={() => handlePokemonToggle(p.name)}
                    disabled={selectedPokemon.length >= 5 && !selectedPokemon.includes(p.name)}
                  />
                  <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    {p.name}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  タイプ: {p.type}
                </Typography>
                
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  きのみ: {p.berry}
                </Typography>
                
                <Box display="flex" flexWrap="wrap" gap={0.5} mb={1}>
                  {p.ingredients.map((ingredient, index) => (
                    <Chip key={index} label={ingredient} size="small" variant="outlined" />
                  ))}
                </Box>
                
                <Typography variant="body2">
                  おてつだい頻度: {p.frequency}秒
                </Typography>
                <Typography variant="body2">
                  スキル確率: {p.skill_probability.toFixed(1)}%
                </Typography>
                <Typography variant="body2">
                  食材確率: {p.ingredient_probability.toFixed(1)}%
                </Typography>
                <Typography variant="body2">
                  持ち物上限: {p.inventory_size}個
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default PokemonList;