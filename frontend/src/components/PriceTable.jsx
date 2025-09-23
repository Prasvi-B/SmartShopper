import React from 'react';

const PriceTable = ({ prices }) => (
  <table className="min-w-full border mt-4">
    <thead>
      <tr>
        <th className="border px-4 py-2">Site</th>
        <th className="border px-4 py-2">Price</th>
      </tr>
    </thead>
    <tbody>
      {prices.map((item, idx) => (
        <tr key={idx}>
          <td className="border px-4 py-2">{item.site}</td>
          <td className="border px-4 py-2">₹{item.price}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default PriceTable;
