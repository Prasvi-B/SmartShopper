import React from 'react'
import { useSearchParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Loader2, Filter, SortAsc } from 'lucide-react'
import { searchProducts } from '../utils/api'
import ProductCard from '../components/ProductCard'
import SearchBar from '../components/SearchBar'

const Results = () => {
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q') || ''

  const { data, isLoading, error } = useQuery({
    queryKey: ['search', query],
    queryFn: () => searchProducts(query),
    enabled: !!query,
  })

  const handleSearch = (newQuery) => {
    setSearchParams({ q: newQuery })
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Searching products...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">Error searching products: {error.message}</p>
        <button 
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Try Again
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      {/* Search Bar */}
      <div className="max-w-2xl mx-auto">
        <SearchBar 
          onSearch={handleSearch} 
          placeholder="Search for products..."
          defaultValue={query}
        />
      </div>

      {/* Results Header */}
      {data && (
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-primary-600 dark:text-accent-blue drop-shadow-glow">
              Search Results for "{query}"
            </h1>
            <p className="text-slate-600 dark:text-gray-50 mt-1">
              Found {data.total_count} products
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="flex items-center px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-card shadow-glass backdrop-blur-xs transition-colors">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </button>
            <button className="flex items-center px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-card shadow-glass backdrop-blur-xs transition-colors">
              <SortAsc className="h-4 w-4 mr-2" />
              Sort
            </button>
          </div>
        </div>
      )}

      {/* Results Grid */}
      {data?.products?.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : query ? (
        <div className="text-center py-12">
          <p className="text-slate-600 dark:text-gray-50 text-lg">No products found for "{query}"</p>
          <p className="text-slate-500 dark:text-gray-50 mt-2">Try searching with different keywords</p>
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-slate-600 dark:text-gray-50 text-lg">Enter a search term to find products</p>
        </div>
      )}
    </div>
  )
}

export default Results
