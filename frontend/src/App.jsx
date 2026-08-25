import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import Analytics from './pages/Analytics'
import Safety from './pages/Safety'
import Scams from './pages/Scams'
import Medical from './pages/Medical'
import Chatbot from './pages/Chatbot'
import Emergency from './pages/Emergency'
import Budget from './pages/Budget'
import Home from './pages/Home'
import Maps from './pages/Maps'
import Planner from './pages/Planner'
import Weather from './pages/Weather'
import CommandCenter from './pages/CommandCenter'
import './App.css'

function App() {
  return <BrowserRouter><Routes><Route element={<DashboardLayout />}><Route index element={<CommandCenter />} /><Route path="overview" element={<Home />} /><Route path="planner" element={<Planner />} /><Route path="maps" element={<Maps />} /><Route path="budget" element={<Budget />} /><Route path="analytics" element={<Analytics />} /><Route path="emergency" element={<Emergency />} /><Route path="weather" element={<Weather />} /><Route path="safety" element={<Safety />} /><Route path="scams" element={<Scams />} /><Route path="medical" element={<Medical />} /><Route path="chatbot" element={<Chatbot />} /><Route path="*" element={<Navigate to="/" replace />} /></Route></Routes></BrowserRouter>
}

export default App
