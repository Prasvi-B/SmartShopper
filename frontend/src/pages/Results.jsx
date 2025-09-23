import React from 'react';
import PriceTable from '../components/PriceTable';
import SentimentChart from '../components/SentimentChart';
import RecommendationCard from '../components/RecommendationCard';

const Results = ({ prices, sentiments, recommendation }) => (
  <div className="max-w-xl mx-auto mt-10">
    <PriceTable prices={prices} />
    <SentimentChart sentiments={sentiments} />
    <RecommendationCard recommendation={recommendation} />
  </div>
);

export default Results;
