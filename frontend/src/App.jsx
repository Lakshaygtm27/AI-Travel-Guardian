import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import Analytics from './pages/Analytics'
import Chatbot from './pages/Chatbot'
import Emergency from './pages/Emergency'
import Home from './pages/Home'
import Maps from './pages/Maps'
import Planner from './pages/Planner'
import './App.css'

function App() {
  return <BrowserRouter><Routes><Route element={<DashboardLayout />}><Route index element={<Home />} /><Route path="planner" element={<Planner />} /><Route path="maps" element={<Maps />} /><Route path="analytics" element={<Analytics />} /><Route path="emergency" element={<Emergency />} /><Route path="chatbot" element={<Chatbot />} /><Route path="*" element={<Navigate to="/" replace />} /></Route></Routes></BrowserRouter>
}

export default App
