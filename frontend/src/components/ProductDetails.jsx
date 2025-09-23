import React from 'react';

const ProductDetails = ({ product, reviews }) => {
  // Simple keyword extraction for pros/cons
  const pros = reviews.filter(r => r.sentiment === 'positive').map(r => r.text).slice(0, 3);
  const cons = reviews.filter(r => r.sentiment === 'negative').map(r => r.text).slice(0, 3);

  return (
    <div className="bg-white rounded shadow p-6 mt-6">
      <h2 className="text-2xl font-bold mb-4">{product}</h2>
      <div className="mb-4">
        <h3 className="font-semibold">Top Pros</h3>
        <ul className="list-disc ml-6">
          {pros.map((p, idx) => <li key={idx}>{p}</li>)}
        </ul>
      </div>
      <div>
        <h3 className="font-semibold">Top Cons</h3>
        <ul className="list-disc ml-6">
          {cons.map((c, idx) => <li key={idx}>{c}</li>)}
        </ul>
      </div>
    </div>
  );
};

export default ProductDetails;
