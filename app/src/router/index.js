import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import PollsPage from '@/pages/PollsPage.vue'
import BoardingPage from '@/pages/BoardingPage.vue'
import { verifyToken, refreshToken } from '@/services/auth'
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
      meta: { requiresAuth: true },
    },
    {
      path: '/lista-embarque',
      name: 'boarding-list',
      component: BoardingPage,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    let isValid = await verifyToken()

    if (!isValid) {
      try {
        await refreshToken()
        isValid = true
      } catch {
        isValid = false
      }
    }

    if (!isValid) return next({ name: 'login' })
  }

  next()
})

export default router
