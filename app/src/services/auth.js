import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/v1/authentication/token/'

// export async function login(email, password) {
//   const response = await axios.post(`${API_URL}`, {
//     username: email,
//     password,
//   })

//   localStorage.setItem('access', response.data.access)
//   localStorage.setItem('refresh', response.data.refresh)

//   return response.data
// }

export async function login(email, password) {
  const response = await fetch(`${API_URL}`, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ username: email, password: password }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.message)
  }

  localStorage.setItem('email', email)
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)

  return data
}

export async function refreshToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) throw new Error('No refresh token')

  const response = await fetch(`${API_URL}refresh`, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ refresh: refresh }),
  })
  const data = await response.json()
  localStorage.setItem('access', data.access)
  return { access: response.data.access }
}

export async function verifyToken() {
  const access = localStorage.getItem('access')
  if (!access) return null

  const response = fetch(`${API_URL}verify`, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ access }),
  })

  const data = response.json()

  if (!response.ok) {
    throw new Error(data.message)
  }

  return data.message
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('email')
}
