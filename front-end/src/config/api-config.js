/**
 * Configuração centralizada das URLs da API
 *
 * Para alterar o ambiente:
 * - Desenvolvimento: use o arquivo .env
 * - Produção: use o arquivo .env.production
 *
 * As variáveis necessárias são:
 * - VITE_APP_API_URL: URL base da API (ex: http://127.0.0.1:8000/api/v1/)
 * - VITE_APP_AUTHENTICATION_URL: URL de autenticação (ex: http://127.0.0.1:8000/api/v1/authentication/token/)
 */

const API_BASE_URL = import.meta.env.VITE_APP_API_URL
const AUTHENTICATION_URL = import.meta.env.VITE_APP_AUTHENTICATION_URL

if (!API_BASE_URL) {
  throw new Error('VITE_APP_API_URL não está definida. Verifique seu arquivo .env')
}

if (!AUTHENTICATION_URL) {
  throw new Error('VITE_APP_AUTHENTICATION_URL não está definida. Verifique seu arquivo .env')
}

export const API_URLS = {
  BASE: API_BASE_URL,
  AUTHENTICATION: AUTHENTICATION_URL,

  // Endpoints específicos
  POLLS: `${API_BASE_URL}polls/`,
  VOTES: `${API_BASE_URL}votes/`,
  STUDENTS: `${API_BASE_URL}students/`,
  TRIPS: `${API_BASE_URL}trips/`,
  BOARDING_POINTS: `${API_BASE_URL}boarding-points/`,
}

export function buildUrl(endpoint) {
  return `${API_BASE_URL}${endpoint}`
}

export function getAuthUrl(path = '') {
  if (!path) return AUTHENTICATION_URL
  return `${AUTHENTICATION_URL}${path}`
}
