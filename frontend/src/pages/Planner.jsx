import { CalendarPlus, CheckCircle2, LoaderCircle } from 'lucide-react'
import { useState } from 'react'
import api from '../services/api'

function diagnosticMessage(error) {
	if (!error.response && error.code === 'ECONNABORTED') return 'Network Error: backend request timed out.'
	if (!error.response) return 'Backend Offline: cannot reach the configured API. Check VITE_API_URL and the backend terminal.'
	if (error.response.status === 404) return 'API Route Missing: /api/itinerary was not found.'
	if (error.response.status === 503 && error.response.data?.detail?.toLowerCase().includes('ollama')) return 'Ollama Offline: the backend cannot reach the AI model.'
	if (error.response.status === 503 && error.response.data?.detail?.toLowerCase().includes('database')) return 'Database Unavailable: check the Supabase connection.'
	if (error.code === 'ERR_NETWORK') return 'Network Error: check the backend URL and CORS settings.'
	return `Network Error: itinerary request failed (${error.response.status}).`
}

export default function Planner() {
	const [form, setForm] = useState({ source_city: 'Delhi', destination_city: 'Jaipur', days: 3, budget: 10000 })
	const [itinerary, setItinerary] = useState('')
	const [notice, setNotice] = useState('')
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState('')
	const generate = async (event) => {
		event.preventDefault(); setLoading(true); setError(''); setNotice('')
		try { const response = await api.post('/api/itinerary', { ...form, days: Number(form.days), budget: Number(form.budget) }); setItinerary(response.data.itinerary); setNotice(response.data.message || '') } catch (requestError) { setError(diagnosticMessage(requestError)) } finally { setLoading(false) }
	}
	return <><div className="page-heading"><div><p className="eyebrow">Plan with intent</p><h1>Your planner</h1><p className="page-subtitle">Build a grounded itinerary with your local travel desk.</p></div></div><section className="panel"><div className="panel-header"><h2>New itinerary</h2><span className="status">AI ready</span></div><form className="planner-form" onSubmit={generate}>{[['source_city','From'],['destination_city','To'],['days','Days'],['budget','Budget (₹)']].map(([name, label]) => <label key={name}>{label}<input required min={name === 'days' ? 1 : undefined} type={name === 'days' || name === 'budget' ? 'number' : 'text'} value={form[name]} onChange={(event) => setForm({ ...form, [name]: event.target.value })} /></label>)}<button className="primary-button" type="submit" disabled={loading}>{loading ? <LoaderCircle className="spin" size={16} /> : <CalendarPlus size={16} />}{loading ? 'Generating itinerary...' : itinerary ? 'Regenerate itinerary' : 'Generate itinerary'}</button></form>{error && <p className="form-error">{error}</p>}{notice && <p className="form-notice">{notice}</p>}</section>{itinerary && <section className="panel itinerary-output"><div className="panel-header"><h2>Your itinerary</h2><span className="status">Generated</span></div><pre>{itinerary}</pre></section>}<section className="panel panel-spaced"><div className="panel-header"><h2>Planning checklist</h2></div><div className="alert"><CheckCircle2 size={17} /><div><strong>Keep your documents together</strong><span>Passport, tickets, and booking confirmations</span></div></div><div className="alert"><CheckCircle2 size={17} /><div><strong>Leave room for local discoveries</strong><span>The best moments rarely make the first draft.</span></div></div></section></>
}
