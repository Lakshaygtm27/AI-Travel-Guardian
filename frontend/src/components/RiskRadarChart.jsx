import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from 'recharts'

const factors = [{ factor: 'Weather', score: 20 }, { factor: 'Medical', score: 10 }, { factor: 'Crowd', score: 15 }, { factor: 'Transport', score: 12 }, { factor: 'Scam', score: 8 }]
export default function RiskRadarChart() { return <ResponsiveContainer width="100%" height={250}><RadarChart data={factors} outerRadius="72%"><PolarGrid stroke="#dce8eb" /><PolarAngleAxis dataKey="factor" tick={{ fill: '#6b8194', fontSize: 11 }} /><PolarRadiusAxis angle={30} domain={[0, 20]} tick={false} axisLine={false} /><Radar name="Risk points" dataKey="score" stroke="#e9785f" fill="#e9785f" fillOpacity={0.42} /><Tooltip /></RadarChart></ResponsiveContainer> }
