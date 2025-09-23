// API helper for backend requests
export async function fetchProductData(query) {
  const res = await fetch(`/api/product?query=${encodeURIComponent(query)}`);
  return res.json();
}

export async function fetchReviewData(productId) {
  const res = await fetch(`/api/reviews?productId=${productId}`);
  return res.json();
}
