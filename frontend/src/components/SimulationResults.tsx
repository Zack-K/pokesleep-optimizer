import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { SimulationResult } from '../types';

interface SimulationResultsProps {
  result: SimulationResult | null;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const SimulationResults: React.FC<SimulationResultsProps> = ({ result }) => {
  if (!result) {
    return (
      <Box textAlign="center" py={4}>
        <Typography variant="h6" color="textSecondary">
          シミュレーション結果がありません
        </Typography>
        <Typography variant="body2" color="textSecondary">
          パーティ最適化タブでシミュレーションを実行してください
        </Typography>
      </Box>
    );
  }

  // 食材データをグラフ用に変換
  const ingredientData = Object.entries(result.ingredients).map(([name, amount]) => ({
    name,
    amount: parseFloat(amount.toFixed(1))
  }));

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        シミュレーション結果
      </Typography>

      <Grid container spacing={3}>
        {/* パーティ情報 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                パーティ編成
              </Typography>
              <List dense>
                {result.party_names.map((name, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={`${index + 1}. ${name}`} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* エナジー情報 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                エナジー統計
              </Typography>
              <Box>
                <Typography variant="body1">
                  総エナジー: {result.total_energy.toFixed(0)}
                </Typography>
                <Typography variant="body1">
                  1日平均: {result.daily_energy.toFixed(0)}
                </Typography>
                <Typography variant="body1">
                  レシピエナジー: {result.recipe_energy.toFixed(0)}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 食材チャート */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              獲得食材
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ingredientData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="name" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="amount" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 食材円グラフ */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              食材構成比
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={ingredientData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="amount"
                >
                  {ingredientData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 作成レシピ */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                作成されたレシピ
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {result.recipes_made.map((recipe, index) => (
                  <Box key={index}>
                    <Typography variant="body2" component="span">
                      {recipe}
                    </Typography>
                    {index < result.recipes_made.length - 1 && (
                      <Typography variant="body2" component="span" sx={{ mx: 1 }}>
                        •
                      </Typography>
                    )}
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SimulationResults;