import React from 'react';

const RecommendationCard = ({ recommendation }) => (
  <div className="bg-green-100 border-l-4 border-green-500 p-4 mt-4">
    <h4 className="font-bold">Best Site to Buy</h4>
    <p>{recommendation}</p>
  </div>
);

export default RecommendationCard;
