import React, { useState } from 'react';

const SortableTable = ({ offers }) => {
  const [sortKey, setSortKey] = useState('price');
  const [sortOrder, setSortOrder] = useState('asc');

  const sortedOffers = [...offers].sort((a, b) => {
    if (sortOrder === 'asc') {
      return a[sortKey] > b[sortKey] ? 1 : -1;
    } else {
      return a[sortKey] < b[sortKey] ? 1 : -1;
    }
  });

  const handleSort = key => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  return (
    <table className="min-w-full border mb-4">
      <thead>
        <tr>
          <th className="border px-4 py-2 cursor-pointer" onClick={() => handleSort('site')}>Site</th>
          <th className="border px-4 py-2 cursor-pointer" onClick={() => handleSort('price')}>Price</th>
          <th className="border px-4 py-2">Link</th>
        </tr>
      </thead>
      <tbody>
        {sortedOffers.map((offer, idx) => (
          <tr key={idx}>
            <td className="border px-4 py-2">{offer.site}</td>
            <td className="border px-4 py-2">₹{offer.price}</td>
            <td className="border px-4 py-2">
              <a href={offer.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">Buy</a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SortableTable;
