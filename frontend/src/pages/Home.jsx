import React from 'react';
import SearchBar from '../components/SearchBar';

const Home = ({ onSearch }) => (
  <div className="max-w-xl mx-auto mt-10">
    <h1 className="text-3xl font-bold mb-6">SmartShopper</h1>
    <SearchBar onSearch={onSearch} />
  </div>
);

export default Home;
