export default function StatCard({ label, value, note, icon: Icon }) {
  return <article className="stat-card"><div className="stat-top"><span>{label}</span><Icon className="stat-icon" size={17} /></div><div className="stat-value">{value}</div><div className="stat-note">{note}</div></article>
}
