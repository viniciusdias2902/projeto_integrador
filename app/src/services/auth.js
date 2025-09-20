import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/v1/authentication/token/'

export async function login(email, password) {
  const response = await axios.post(`${API_URL}`, {
    username: email,
    password,
  })

  localStorage.setItem('access', response.data.access)
  localStorage.setItem('refresh', response.data.refresh)

  return response.data
}

export async function refreshToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) throw new Error('No refresh token')

  const response = await axios.post(`${API_URL}refresh`, { refresh })
  localStorage.setItem('access', response.data.access)
  return { access: response.data.access }
}

export async function verifyToken() {
  const access = localStorage.getItem('access')
  if (!access) return null

  try {
    await axios.post(`${API_URL}verify`, { token: access })
    return true
  } catch {
    return false
  }
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}
