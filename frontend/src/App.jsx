import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')

  useEffect(() => {
    // Check API health on mount
    fetch('/api')
      .then(res => res.json())
      .then(data => {
        setApiStatus(`Connected to ${data.message} v${data.version}`)
      })
      .catch(err => {
        setApiStatus('API connection failed')
        console.error('API Error:', err)
      })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>VC Job Scraper</h1>
        <p className="api-status">API Status: {apiStatus}</p>
        <div className="placeholder">
          <h2>Coming Soon</h2>
          <p>Job scraping and tracking features will be added here.</p>
        </div>
      </header>
    </div>
  )
}

export default App
