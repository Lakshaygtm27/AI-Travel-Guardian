import axios from 'axios'

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:8002').replace(/\/$/, ''),
  timeout: 20000,
})

export function isHealthyResponse(response) {
  const data = response?.data
  return response?.status === 200 && data !== null && typeof data === 'object'
    && (data.status === 'ok' || data.status === 'healthy' || data.success === true || data.service)
}

export async function checkHealth(path) {
  const response = await api.get(path)
  console.log('Health Response', response)
  console.log('Health JSON', response.data)
  return isHealthyResponse(response)
}

export default api
