import React, { useState } from 'react';

const suggestions = [
  'iPhone 15', 'Samsung Galaxy S23', 'MacBook Air', 'Sony WH-1000XM5', 'Nike Air Max'
];

const AutocompleteSearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [filtered, setFiltered] = useState([]);

  const handleChange = e => {
    const val = e.target.value;
    setQuery(val);
    setFiltered(val ? suggestions.filter(s => s.toLowerCase().includes(val.toLowerCase())) : []);
  };

  return (
    <div className="relative w-full max-w-md">
      <input
        type="text"
        className="border rounded px-3 py-2 w-full"
        placeholder="Search for a product..."
        value={query}
        onChange={handleChange}
      />
      {filtered.length > 0 && (
        <ul className="absolute left-0 right-0 bg-white border mt-1 z-10">
          {filtered.map((s, idx) => (
            <li key={idx} className="px-3 py-2 cursor-pointer hover:bg-gray-100" onClick={() => { setQuery(s); setFiltered([]); onSearch(s); }}>{s}</li>
          ))}
        </ul>
      )}
      <button className="bg-blue-500 text-white px-4 py-2 rounded mt-2" onClick={() => onSearch(query)}>Search</button>
    </div>
  );
};

export default AutocompleteSearchBar;
