import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

const SentimentChart = ({ sentiments = { positive: 0, negative: 0, neutral: 0 } }) => {
  const data = [
    { 
      name: 'Positive', 
      value: sentiments.positive, 
      color: '#10B981',
      icon: TrendingUp
    },
    { 
      name: 'Negative', 
      value: sentiments.negative, 
      color: '#EF4444',
      icon: TrendingDown
    },
    { 
      name: 'Neutral', 
      value: sentiments.neutral, 
      color: '#6B7280',
      icon: Minus
    }
  ]

  const total = sentiments.positive + sentiments.negative + sentiments.neutral

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0]
      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg">
          <p className="font-medium" style={{ color: data.payload.color }}>
            {data.name}: {data.value}%
          </p>
        </div>
      )
    }
    return null
  }

  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    if (percent < 0.05) return null // Don't show labels for very small slices
    
    const RADIAN = Math.PI / 180
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize="12"
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  if (total === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No sentiment data available</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend with icons and percentages */}
      <div className="grid grid-cols-3 gap-4">
        {data.map((item) => {
          const IconComponent = item.icon
          return (
            <div key={item.name} className="text-center">
              <div className="flex items-center justify-center mb-2">
                <div 
                  className="w-3 h-3 rounded-full mr-2" 
                  style={{ backgroundColor: item.color }}
                />
                <IconComponent className="h-4 w-4" style={{ color: item.color }} />
              </div>
              <div className="text-sm font-medium text-gray-900">{item.name}</div>
              <div className="text-lg font-bold" style={{ color: item.color }}>
                {item.value}%
              </div>
            </div>
          )
        })}
      </div>

      {/* Summary */}
      <div className="text-center pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          Overall sentiment: {' '}
          <span className={`font-medium ${
            sentiments.positive > sentiments.negative + sentiments.neutral ? 'text-green-600' :
            sentiments.negative > sentiments.positive + sentiments.neutral ? 'text-red-600' :
            'text-gray-600'
          }`}>
            {sentiments.positive > sentiments.negative + sentiments.neutral ? 'Positive' :
             sentiments.negative > sentiments.positive + sentiments.neutral ? 'Negative' :
             'Mixed'}
          </span>
        </p>
      </div>
    </div>
  )
}

export default SentimentChart
