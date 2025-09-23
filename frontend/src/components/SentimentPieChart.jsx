import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts';

const COLORS = ['#22c55e', '#ef4444', '#fbbf24'];

const SentimentPieChart = ({ sentiments }) => {
  const data = [
    { name: 'Positive', value: sentiments.positive },
    { name: 'Negative', value: sentiments.negative },
    { name: 'Neutral', value: sentiments.neutral },
  ];
  return (
    <PieChart width={320} height={220}>
      <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
        {data.map((entry, idx) => (
          <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
        ))}
      </Pie>
      <Legend />
      <Tooltip />
    </PieChart>
  );
};

export default SentimentPieChart;
