import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import App from './App.jsx'
import VehicleStatsPage from './vehicle-stats.jsx'
import CharacterStatsPage from './character-stats.jsx'
import './App.css'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter basename="/combo-compare">
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/vehicles" element={<VehicleStatsPage />} />
        <Route path="/characters" element={<CharacterStatsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
