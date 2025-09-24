import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Star, ExternalLink, TrendingDown, TrendingUp, Minus } from 'lucide-react'
import { getProduct, getProductReviews } from '../utils/api'
import SentimentChart from '../components/SentimentChart'
import PriceTable from '../components/PriceTable'

const ProductDetails = () => {
  const { id } = useParams()

  const { data: product, isLoading: productLoading } = useQuery({
    queryKey: ['product', id],
    queryFn: () => getProduct(id),
  })

  const { data: reviews, isLoading: reviewsLoading } = useQuery({
    queryKey: ['reviews', id],
    queryFn: () => getProductReviews(id),
  })

  if (productLoading || reviewsLoading) {
    return <div className="text-center py-12">Loading product details...</div>
  }

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return <TrendingUp className="h-4 w-4 text-green-600" />
      case 'negative':
        return <TrendingDown className="h-4 w-4 text-red-600" />
      default:
        return <Minus className="h-4 w-4 text-gray-600" />
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Product Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex flex-col md:flex-row gap-6">
          <div className="md:w-1/3">
            <img
              src={product?.image_url || '/api/placeholder/300/300'}
              alt={product?.name}
              className="w-full h-64 object-cover rounded-lg"
            />
          </div>
          <div className="md:w-2/3">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{product?.name}</h1>
            <p className="text-gray-600 mb-4">{product?.description}</p>
            <div className="flex items-center space-x-4 mb-4">
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                {product?.brand}
              </span>
              <div className="flex items-center">
                <Star className="h-4 w-4 text-yellow-400 fill-current" />
                <span className="ml-1 text-gray-600">4.5 out of 5</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Price Comparison */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Price Comparison</h2>
        <PriceTable offers={[]} />
      </div>

      {/* Reviews & Sentiment */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Sentiment Analysis */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Review Sentiment</h2>
          <SentimentChart sentiments={{ positive: 65, negative: 15, neutral: 20 }} />
        </div>

        {/* Recent Reviews */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Reviews</h2>
          <div className="space-y-4">
            {reviews?.slice(0, 3).map((review) => (
              <div key={review.id} className="border-b border-gray-200 pb-4 last:border-b-0">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900">{review.reviewer_name}</span>
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-4 w-4 ${
                            i < review.rating
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    {getSentimentIcon(review.sentiment_label)}
                    <span className="text-sm text-gray-600 capitalize">
                      {review.sentiment_label}
                    </span>
                  </div>
                </div>
                <h4 className="font-medium text-gray-900 mb-1">{review.title}</h4>
                <p className="text-gray-600 text-sm">{review.content}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetails