import { BarChart3, Bot, CalendarDays, Map, ShieldAlert, WalletCards } from 'lucide-react'
import { NavLink } from 'react-router-dom'

const links = [['/', 'Overview', BarChart3], ['planner', 'Planner', CalendarDays], ['maps', 'Maps', Map], ['analytics', 'Analytics', WalletCards], ['emergency', 'Emergency', ShieldAlert], ['chatbot', 'Travel desk', Bot]]

export default function Sidebar() {
  return <aside className="sidebar"><div className="section-label">Workspace</div><nav className="nav-list">{links.map(([to, label, Icon]) => <NavLink key={label} to={to} end={to === '/'} className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}><Icon size={17} /><span>{label}</span></NavLink>)}</nav><div className="sidebar-bottom"><p>Your next adventure is 18 days away.</p><button type="button">Open itinerary</button></div></aside>
}
