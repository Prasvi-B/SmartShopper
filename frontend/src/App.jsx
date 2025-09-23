import React, { useState } from 'react';
import { useSearch } from './api';
import AutocompleteSearchBar from './components/AutocompleteSearchBar';
import SortableTable from './components/SortableTable';

function App() {
  const [query, setQuery] = useState('');
  const { data, isLoading, error } = useSearch(query);

  const handleSearch = q => setQuery(q);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold mb-6">SmartShopper</h1>
      <AutocompleteSearchBar onSearch={handleSearch} />
      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
      {data && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-2">Results for: {data.product}</h2>
          <SortableTable offers={data.offers} />
          <div className="mb-4">
            <h3 className="font-bold mb-2">Review Sentiment</h3>
            <ul className="mb-2">
              <li>Positive: {data.review_sentiments.positive}</li>
              <li>Negative: {data.review_sentiments.negative}</li>
              <li>Neutral: {data.review_sentiments.neutral}</li>
            </ul>
            <SentimentPieChart sentiments={data.review_sentiments} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
