import React from 'react'
import { Link } from 'react-router-dom'
import { Star, ExternalLink, TrendingUp, TrendingDown, Minus } from 'lucide-react'

const ProductCard = ({ product }) => {
  const getSentimentColor = (avgSentiment) => {
    if (avgSentiment > 0.3) return 'text-green-600 bg-green-50'
    if (avgSentiment < -0.3) return 'text-red-600 bg-red-50'
    return 'text-gray-600 bg-gray-50'
  }

  const getSentimentIcon = (avgSentiment) => {
    if (avgSentiment > 0.3) return <TrendingUp className="h-4 w-4" />
    if (avgSentiment < -0.3) return <TrendingDown className="h-4 w-4" />
    return <Minus className="h-4 w-4" />
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price)
  }

  return (
    <div className="group bg-white/70 dark:bg-dark-card/70 backdrop-blur-lg rounded-2xl shadow-glass hover:shadow-glow-lg transition-all duration-500 border border-white/20 dark:border-slate-700/50 animate-fadeInUp hover:scale-[1.02] overflow-hidden">
      <div className="p-6">
        {/* Product Image */}
        <div className="aspect-square w-full mb-6 overflow-hidden rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 dark:from-dark-bg dark:to-dark-surface shadow-inner">
          <img
            src={product.image_url || '/api/placeholder/200/200'}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
          />
        </div>

        {/* Product Info */}
        <div className="space-y-4">
          <div>
            <h3 className="font-bold text-lg bg-gradient-accent bg-clip-text text-transparent line-clamp-2 group-hover:scale-105 transition-transform duration-300">
              <Link to={`/product/${product.id}`}>
                {product.name}
              </Link>
            </h3>
            {product.brand && (
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-2 font-medium">{product.brand}</p>
            )}
          </div>

          {/* Price Range */}
          <div className="flex items-center justify-between">
            <div>
              <span className="text-2xl font-bold bg-gradient-accent bg-clip-text text-transparent">
                {formatPrice(product.min_price)}
              </span>
              {product.min_price !== product.max_price && (
                <span className="text-sm text-slate-500 dark:text-slate-400 ml-2 line-through">
                  {formatPrice(product.max_price)}
                </span>
              )}
            </div>
            {product.best_offer?.discount_percentage > 0 && (
              <span className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-glow animate-glow">
                {product.best_offer.discount_percentage.toFixed(0)}% OFF
              </span>
            )}
          </div>

          {/* Rating and Reviews */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1">
              <Star className="h-4 w-4 text-amber-500 fill-current" />
              <span className="text-sm text-slate-600 dark:text-gray-50">
                {product.avg_rating.toFixed(1)} ({product.total_reviews})
              </span>
            </div>

            {/* Sentiment Indicator */}
            <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs shadow-glass backdrop-blur-xs ${getSentimentColor(product.sentiment_summary?.avg_sentiment || 0)}`}>
              {getSentimentIcon(product.sentiment_summary?.avg_sentiment || 0)}
              <span>
                {product.sentiment_summary?.positive || 0}% positive
              </span>
            </div>
          </div>

          {/* Best Offer */}
          {product.best_offer && (
            <div className="pt-3 border-t border-slate-100 dark:border-slate-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <img
                    src={`/api/placeholder/20/20`}
                    alt={product.best_offer.platform}
                    className="w-5 h-5 rounded"
                  />
                  <span className="text-sm text-slate-600 dark:text-gray-50 capitalize">
                    {product.best_offer.platform}
                  </span>
                </div>
                <a
                  href={product.best_offer.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 text-primary-600 dark:text-accent-blue hover:text-accent-purple text-sm"
                >
                  <span>View Deal</span>
                  <ExternalLink className="h-3 w-3" />
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProductCard