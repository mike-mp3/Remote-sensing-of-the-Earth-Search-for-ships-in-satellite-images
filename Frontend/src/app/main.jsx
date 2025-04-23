import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// import '@/shared/global_styles/index.css'
import '@/shared/global_styles/_global.module.scss'
import App from '@/app/App'
import { BrowserRouter } from 'react-router-dom'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
