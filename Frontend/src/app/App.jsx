import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState } from 'react'
import '@/shared/global_styles/_global.module.scss';
import { LoginPage } from '@/pages/LoginPage';
import { RegistrationPage } from '@/pages/RegistrationPage';
import { ConfirmPage } from "@/pages/ConfirmPage";

function App() {
  const [count, setCount] = useState(0)

  return (
    <Routes>
    <Route path="/" element={<LoginPage/>}/>
    <Route path="/signup" element={< RegistrationPage/>} />
    <Route path="/confirm" element={< ConfirmPage/>} />
  </Routes>
  )
}

export default App
