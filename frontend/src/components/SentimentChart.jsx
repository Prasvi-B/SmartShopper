import React from 'react';

const SentimentChart = ({ sentiments }) => {
  // Dummy pie chart (replace with chart lib later)
  const total = sentiments.positive + sentiments.negative + sentiments.neutral;
  return (
    <div className="mt-4">
      <h3 className="font-bold mb-2">Review Sentiment</h3>
      <ul>
        <li>Positive: {((sentiments.positive/total)*100).toFixed(1)}%</li>
        <li>Negative: {((sentiments.negative/total)*100).toFixed(1)}%</li>
        <li>Neutral: {((sentiments.neutral/total)*100).toFixed(1)}%</li>
      </ul>
    </div>
  );
};

export default SentimentChart;
