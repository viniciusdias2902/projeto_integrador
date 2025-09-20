import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000//api/v1/authentication/'

export async function login(email, password) {
  console.log('Teste')
  const response = await axios.post(`${API_URL}token/`, {
    email,
    password,
  })

  localStorage.setItem('access', response.data.access)
  localStorage.setItem('refresh', response.data.refresh)

  return response.data
}

export async function refreshToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) return null

  const response = await axios.post(`${API_URL}token/refresh/`, {
    refresh,
  })

  localStorage.setItem('access', response.data.access)
  return response.data
}

export async function verifyToken() {
  const access = localStorage.getItem('access')
  if (!access) return null

  try {
    await axios.post(`${API_URL}token/verify/`, { token: access })
    return true
  } catch {
    return false
  }
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}
