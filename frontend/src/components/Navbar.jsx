import { Bell, Compass } from 'lucide-react'

export default function Navbar() {
  return <header className="topbar"><a className="brand" href="/"><span className="brand-mark"><Compass size={18} /></span>Voyanta</a><div className="topbar-right"><button className="icon-button" aria-label="Notifications"><Bell size={18} /></button><div className="profile"><span>Alex Morgan</span><div className="avatar">AM</div></div></div></header>
}
