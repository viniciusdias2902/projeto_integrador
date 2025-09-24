const URL = import.meta.env.VITE_APP_AUTHENTICATION_URL

export async function login(email, password) {
  const response = await fetch(`${URL}`, {
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

  const response = await fetch(`${URL}refresh`, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ refresh: refresh }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.message)
  }

  localStorage.setItem('access', data.access)
}

export async function verifyToken() {
  const access = localStorage.getItem('access')
  if (!access) return false

  const response = await fetch(`${URL}verify`, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ token: access }),
  })

  if (!response.ok) {
    return false
  }

  return true
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('email')
}
