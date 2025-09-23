import React from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = React.useState('');
  return (
    <div className="flex items-center gap-2">
      <input
        type="text"
        className="border rounded px-3 py-2 w-full"
        placeholder="Search for a product..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={() => onSearch(query)}
      >
        Search
      </button>
    </div>
  );
};

export default SearchBar;
