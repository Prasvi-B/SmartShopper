import React, { useState } from 'react';

const PriceDropAlert = ({ product }) => {
  const [email, setEmail] = useState('');
  const [price, setPrice] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = e => {
    e.preventDefault();
    // TODO: Call backend to save alert
    setSubmitted(true);
  };

  return (
    <form className="bg-blue-50 p-4 rounded mt-4" onSubmit={handleSubmit}>
      <h4 className="font-bold mb-2">Set Price Drop Alert for {product}</h4>
      <input
        type="email"
        className="border rounded px-3 py-2 mr-2"
        placeholder="Your email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <input
        type="number"
        className="border rounded px-3 py-2 mr-2"
        placeholder="Target price (INR)"
        value={price}
        onChange={e => setPrice(e.target.value)}
        required
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Set Alert</button>
      {submitted && <p className="text-green-600 mt-2">Alert set! You'll be notified when price drops.</p>}
    </form>
  );
};

export default PriceDropAlert;
