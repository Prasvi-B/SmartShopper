import React from 'react'
import { ExternalLink, Star, Truck, Shield } from 'lucide-react'

const PriceTable = ({ offers = [] }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price)
  }

  const getPlatformLogo = (platform) => {
    // In a real app, you'd have actual platform logos
    const colors = {
      amazon: 'bg-orange-500',
      flipkart: 'bg-blue-500',
      myntra: 'bg-pink-500',
    }
    return colors[platform] || 'bg-gray-500'
  }

  if (!offers || offers.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No price data available</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Platform</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Price</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Discount</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Seller</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Shipping</th>
            <th className="text-right py-3 px-4 font-semibold text-gray-900">Action</th>
          </tr>
        </thead>
        <tbody>
          {offers.map((offer, index) => (
            <tr key={offer.id || index} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="py-4 px-4">
                <div className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-full ${getPlatformLogo(offer.platform)} flex items-center justify-center`}>
                    <span className="text-white text-xs font-bold">
                      {offer.platform.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="font-medium text-gray-900 capitalize">
                    {offer.platform}
                  </span>
                </div>
              </td>
              
              <td className="py-4 px-4">
                <div>
                  <span className="text-lg font-bold text-gray-900">
                    {formatPrice(offer.price)}
                  </span>
                  {offer.original_price && offer.original_price > offer.price && (
                    <div className="text-sm text-gray-500 line-through">
                      {formatPrice(offer.original_price)}
                    </div>
                  )}
                </div>
              </td>
              
              <td className="py-4 px-4">
                {offer.discount_percentage > 0 ? (
                  <span className="bg-green-100 text-green-800 text-sm px-2 py-1 rounded-full">
                    {offer.discount_percentage.toFixed(0)}% off
                  </span>
                ) : (
                  <span className="text-gray-400">-</span>
                )}
              </td>
              
              <td className="py-4 px-4">
                <div className="flex items-center space-x-1">
                  <span className="text-gray-700">{offer.seller_name}</span>
                  {offer.seller_name === 'Amazon' || offer.seller_name === 'Flipkart' ? (
                    <Shield className="h-4 w-4 text-green-600" title="Trusted seller" />
                  ) : null}
                </div>
              </td>
              
              <td className="py-4 px-4">
                <div className="flex items-center space-x-1">
                  <Truck className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    {offer.shipping_cost === 0 ? 'Free' : formatPrice(offer.shipping_cost)}
                  </span>
                </div>
              </td>
              
              <td className="py-4 px-4 text-right">
                <a
                  href={offer.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <span>Buy Now</span>
                  <ExternalLink className="h-4 w-4" />
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default PriceTable
