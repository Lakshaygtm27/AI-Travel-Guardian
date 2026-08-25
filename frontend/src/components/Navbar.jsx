import { Bell, Compass } from 'lucide-react'
import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Navbar() {
  const [health, setHealth] = useState({ backend: false, ollama: false, database: false })
  useEffect(() => {
    let mounted = true
    Promise.allSettled([api.get('/health'), api.get('/health/ollama'), api.get('/health/database')]).then((results) => {
      if (mounted) setHealth({ backend: results[0].status === 'fulfilled', ollama: results[1].status === 'fulfilled', database: results[2].status === 'fulfilled' })
    })
    return () => { mounted = false }
  }, [])
  return <header className="topbar"><a className="brand" href="/"><span className="brand-mark"><Compass size={18} /></span>AI Travel Guardian 360</a><div className="topbar-right"><div className="health-indicators" aria-label="Service status"><span className={health.backend ? 'online' : 'offline'}><i /> API {health.backend ? 'Online' : 'Offline'}</span><span className={health.ollama ? 'online' : 'offline'}><i /> AI {health.ollama ? 'Online' : 'Offline'}</span><span className={health.database ? 'online' : 'offline'}><i /> DB {health.database ? 'Online' : 'Offline'}</span></div><button className="icon-button" aria-label="Notifications"><Bell size={18} /></button><div className="profile"><span>Alex Morgan</span><div className="avatar">AM</div></div></div></header>
}
