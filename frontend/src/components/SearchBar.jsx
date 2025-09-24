import React, { useState } from 'react'
import { Search } from 'lucide-react'

const SearchBar = ({ onSearch, placeholder = "Search products...", defaultValue = "" }) => {
  const [input, setInput] = useState(defaultValue)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSearch(input.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative animate-fadeInUp group">
      <div className="relative flex items-center">
        <Search className="absolute left-5 h-6 w-6 text-primary-500 dark:text-accent-blue z-10" />
        <input
          id="search-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-14 pr-32 py-5 text-lg bg-white/70 dark:bg-dark-card/70 backdrop-blur-lg border border-white/20 dark:border-slate-700/50 rounded-2xl focus:ring-4 focus:ring-primary-500/20 dark:text-white shadow-glass-lg focus:shadow-glow-lg focus:border-primary-500 dark:focus:border-accent-blue outline-none transition-all duration-300 placeholder:text-slate-400 dark:placeholder:text-slate-500"
        />
        <button
          type="submit"
          className="absolute right-3 px-8 py-3 bg-gradient-accent text-white font-semibold rounded-xl shadow-glow hover:shadow-glow-lg hover:scale-105 focus:scale-105 transition-all duration-300 animate-glow"
        >
          Search
        </button>
      </div>
    </form>
  )
}

export default SearchBar
