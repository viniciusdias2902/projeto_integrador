import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import PollsPage from '@/pages/PollsPage.vue'
import BoardingPage from '@/pages/BoardingPage.vue'
import RegistrationPage from '@/pages/RegistrationPage.vue'
import TripsPage from '@/pages/TripsPage.vue'
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
      path: '/cadastro',
      name: 'registration-page',
      component: RegistrationPage,
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  // Verificar se a rota requer autenticação
  if (to.meta.requiresAuth) {
    const isValid = await verifyAndRefreshToken()

    if (!isValid) {
      return next({ name: 'login' })
    }

    if (to.meta.allowedRoles) {
      const userRole = getUserRole()

      if (!userRole || !to.meta.allowedRoles.includes(userRole)) {
        if (userRole === 'student') {
          return next({ name: 'polls' })
        } else if (userRole === 'driver') {
          return next({ name: 'trips' })
        } else {
          return next({ name: 'login' })
        }
      }
    }
  }

  next()
})

export default router
