import { ref, computed } from 'vue'
import { decodeJwt } from '@/services/auth'

const userRole = ref(null)

export function useAuth() {
  function getRoleFromToken() {
    const token = localStorage.getItem('access')
    if (!token) {
      userRole.value = null
      return null
    }

    try {
      const decoded = decodeJwt(token)
      userRole.value = decoded.role
      return decoded.role
    } catch (error) {
      console.error('Error decoding token:', error)
      userRole.value = null
      return null
    }
  }

  function updateRole() {
    return getRoleFromToken()
  }

  const isStudent = computed(() => userRole.value === 'student')
  const isDriver = computed(() => userRole.value === 'driver')
  const isAuthenticated = computed(() => !!localStorage.getItem('access'))

  if (!userRole.value && localStorage.getItem('access')) {
    getRoleFromToken()
  }

  return {
    userRole,
    isStudent,
    isDriver,
    isAuthenticated,
    getRoleFromToken,
    updateRole,
  }
}
