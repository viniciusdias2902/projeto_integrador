import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import PollsPage from '@/pages/PollsPage.vue'
import BoardingPage from '@/pages/BoardingPage.vue'
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
    },
    {
      path: '/lista-embarque',
      name: 'boarding-list',
      component: BoardingPage,
    },
  ],
})

export default router
