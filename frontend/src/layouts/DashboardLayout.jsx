import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'

export default function DashboardLayout() {
  return <div className="app-shell"><Navbar /><div className="workspace"><Sidebar /><main className="main-content"><Outlet /></main></div></div>
}
