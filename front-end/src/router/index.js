import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import PollsPage from '@/pages/PollsPage.vue'
import BoardingPage from '@/pages/BoardingPage.vue'
import RegistrationPage from '@/pages/RegistrationPage.vue'
import TripsPage from '@/pages/TripsPage.vue'
import TripViewPage from '@/pages/TripViewPage.vue'
import AdminStudentsPage from '@/pages/AdminStudentsPage.vue'
import AdminDashboardPage from '@/pages/AdminDashboardPage.vue'
import { verifyAndRefreshToken, getUserRole } from '@/services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/enquetes',
      name: 'polls',
      component: PollsPage,
      meta: { requiresAuth: true, allowedRoles: ['student'] },
    },
    {
      path: '/lista-embarque',
      name: 'boarding-list',
      component: BoardingPage,
      meta: { requiresAuth: true, allowedRoles: ['student', 'driver'] },
    },
    {
      path: '/viagens',
      name: 'trips',
      component: TripsPage,
      meta: { requiresAuth: true, allowedRoles: ['driver'] },
    },
    {
      path: '/acompanhar-viagem',
      name: 'trip-view',
      component: TripViewPage,
      meta: { requiresAuth: true, allowedRoles: ['student'] },
    },
    {
      path: '/admin/estudantes',
      name: 'admin-students',
      component: AdminStudentsPage,
      meta: { requiresAuth: true, allowedRoles: ['admin'] },
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardPage,
      meta: { requiresAuth: true, allowedRoles: ['admin'] },
    },
    {
      path: '/cadastro',
      name: 'registration-page',
      component: RegistrationPage,
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  console.log('Router guard - navigating to:', to.path)

  if (to.meta.requiresAuth) {
    const isValid = await verifyAndRefreshToken()

    if (!isValid) {
      console.log('Token invalid, redirecting to login')
      return next({ name: 'login' })
    }

    if (to.meta.allowedRoles) {
      const userRole = getUserRole()
      const normalizedRole = (userRole || '').toLowerCase()

      console.log('User role:', userRole)
      console.log('Normalized role:', normalizedRole)
      console.log('Allowed roles:', to.meta.allowedRoles)

      const normalizedAllowedRoles = to.meta.allowedRoles.map((role) => role.toLowerCase())

      if (!userRole || !normalizedAllowedRoles.includes(normalizedRole)) {
        console.log('Role not allowed, redirecting...')

        if (normalizedRole === 'student') {
          return next({ name: 'polls' })
        } else if (normalizedRole === 'driver') {
          return next({ name: 'trips' })
        } else if (normalizedRole === 'admin') {
          return next({ name: 'admin-students' })
        } else {
          return next({ name: 'login' })
        }
      }
    }
  }

  next()
})

export default router
