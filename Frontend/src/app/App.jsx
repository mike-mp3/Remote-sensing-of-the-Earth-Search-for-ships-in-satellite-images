import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import '@/shared/global_styles/App.css'


function App() {
  const [count, setCount] = useState(0)

  return (
    <Routes>
    <Route path="/" element={<LoginPage />} />
    <Route path="/home" element={<HomePage />} />
  </Routes>
  )
}

export default App
