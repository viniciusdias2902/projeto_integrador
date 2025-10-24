import { API_URLS, getAuthUrl } from '@/config/api-config'

export async function login(email, password) {
  const response = await fetch(API_URLS.AUTHENTICATION, {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ username: email, password: password }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.message)
  }

  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)
  localStorage.setItem('role', data.role)

  return data
}

export async function refreshToken() {
  const refresh = localStorage.getItem('refresh')
  if (!refresh) throw new Error('No refresh token')

  const response = await fetch(getAuthUrl('refresh'), {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ refresh: refresh }),
  })

  const data = await response.json()

  if (!response.ok) {
    logout()
    throw new Error(data.message || 'Invalid refresh token ')
  }

  localStorage.setItem('access', data.access)
}

export async function verifyToken() {
  const access = localStorage.getItem('access')
  if (!access) return false

  const response = await fetch(getAuthUrl('verify'), {
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
  localStorage.removeItem('role')
}

export async function verifyAndRefreshToken() {
  let isValid = await verifyToken()

  if (!isValid) {
    try {
      await refreshToken()
      isValid = true
    } catch {
      isValid = false
    }
  }

  return isValid
}

export function decodeJwt(token) {
  const payload = token.split('.')[1]
  const decoded = atob(payload)
  return JSON.parse(decoded)
}

export function getUserRole() {
  const role = localStorage.getItem('role')
  if (role) return role

  const token = localStorage.getItem('access')
  if (token) {
    try {
      const decoded = decodeJwt(token)
      return decoded.role
    } catch {
      return null
    }
  }

  return null
}
