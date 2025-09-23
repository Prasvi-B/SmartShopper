import { useQuery } from 'react-query';

export const fetchSearchResults = async (query) => {
  const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error('Network response was not ok');
  return res.json();
};

export const useSearch = (query) => {
  return useQuery(['search', query], () => fetchSearchResults(query), {
    enabled: !!query,
  });
};
