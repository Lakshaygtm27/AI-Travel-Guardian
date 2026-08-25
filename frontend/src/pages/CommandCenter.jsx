import { AlertTriangle, CloudRain, MapPin, RefreshCw, ShieldCheck, Siren, WalletCards } from 'lucide-react'
import { useEffect, useEffectEvent, useState } from 'react'
import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet'
import RiskRadarChart from '../components/RiskRadarChart'
import api from '../services/api'
import 'leaflet/dist/leaflet.css'

const markers = [
  { name: 'Amber Fort', type: 'Attraction', position: [26.9855, 75.8513], color: '#27a66f' },
  { name: 'City Palace', type: 'Attraction', position: [26.9258, 75.8237], color: '#27a66f' },
  { name: 'Sawai Man Singh Hospital', type: 'Hospital', position: [26.9005, 75.8056], color: '#d64b61' },
  { name: 'Rambagh Palace', type: 'Hotel', position: [26.8915, 75.8067], color: '#3b6ea5' },
  { name: 'Ashok Nagar Police', type: 'Police', position: [26.9092, 75.7956], color: '#e9785f' },
  { name: '24Seven Pharmacy', type: 'Pharmacy', position: [26.912, 75.787], color: '#8b5cc7' },
]

export default function CommandCenter() {
  const [weather, setWeather] = useState(null)
  const [replan, setReplan] = useState(null)
  const loadWeather = useEffectEvent(async () => {
    const response = await api.get('/weather/Jaipur')
    setWeather(response.data)
  })
  useEffect(() => {
    loadWeather().catch(() => {})
    const refreshTimer = setInterval(() => loadWeather().catch(() => {}), 30000)
    return () => clearInterval(refreshTimer)
  }, [])
  const runReplan = async () => {
    const response = await api.post('/replan-trip', { rain: weather?.rain || 0 })
    setReplan(response.data)
  }
  return <><div className="page-heading"><div><p className="eyebrow">Live travel intelligence</p><h1>Command center</h1><p className="page-subtitle">One calm view of the signals shaping your Jaipur trip.</p></div><button className="primary-button" type="button" onClick={runReplan}><RefreshCw size={16} /> Replan trip</button></div><div className="command-metrics"><article className="command-metric"><span><WalletCards size={16} /> Budget</span><strong>₹6,000 <small>/ ₹10,000</small></strong><em>60% used</em></article><article className="command-metric"><span><CloudRain size={16} /> Weather</span><strong>{weather ? `${weather.temperature}°C` : '32°C'}</strong><em>{weather ? `${weather.rain} mm rain · ${weather.wind} km/h wind` : 'Loading live data'}</em></article><article className="command-metric"><span><AlertTriangle size={16} /> Risk score</span><strong>65 <small>/ 100</small></strong><em className="medium-risk">Medium risk</em></article><article className="command-metric"><span><ShieldCheck size={16} /> Safety</span><strong>Good</strong><em>3 safe zones nearby</em></article></div>{replan?.changed && <div className="replan-banner"><CloudRain size={19} /><div><strong>Dynamic replan suggested</strong><span>{replan.replace} → {replan.with} because rain is expected.</span></div></div>}<div className="command-layout"><section className="panel command-map"><div className="panel-header"><h2>Live Jaipur map</h2><span className="status">5 layers active</span></div><MapContainer center={[26.9124, 75.7873]} zoom={12} scrollWheelZoom className="command-leaflet"><TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />{markers.map((marker) => <CircleMarker key={marker.name} center={marker.position} radius={8} pathOptions={{ color: marker.color, fillColor: marker.color, fillOpacity: .9 }}><Popup><strong>{marker.name}</strong><br />{marker.type}<br />Live location context.</Popup></CircleMarker>)}</MapContainer><div className="map-legend">{[['Attractions','#27a66f'],['Hotels','#3b6ea5'],['Hospitals','#d64b61'],['Police','#e9785f'],['Pharmacies','#8b5cc7']].map(([label, color]) => <span key={label}><i style={{ background: color }} />{label}</span>)}</div></section><section className="panel radar-panel"><div className="panel-header"><h2>Risk radar</h2><span className="status warning-status">Medium</span></div><RiskRadarChart /><div className="risk-total"><strong>65</strong><span>total risk points</span></div></section></div><div className="command-bottom"><section className="panel"><div className="panel-header"><h2>Alerts</h2><span className="panel-link">View all</span></div><div className="command-alert"><AlertTriangle size={17} /><div><strong>Common scam: fake guides</strong><span>Keep official tickets visible.</span></div></div><div className="command-alert"><CloudRain size={17} /><div><strong>Weather monitored live</strong><span>Next refresh in 30 seconds.</span></div></div></section><section className="panel"><div className="panel-header"><h2>Recommendation</h2></div><div className="recommendation"><MapPin size={19} /><div><strong>Keep Amber Fort flexible</strong><span>Check the morning forecast before leaving. Albert Hall Museum is your indoor backup.</span></div></div></section><section className="sos-panel"><Siren size={25} /><div><strong>Need help now?</strong><span>Share your location with emergency services.</span></div><a className="sos-small" href="/emergency">SOS</a></section></div></>
}
