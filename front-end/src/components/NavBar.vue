<script setup>
import { useRoute } from 'vue-router'
import { logout } from '@/services/auth'
import { useAuth } from '@/useAuth'

const route = useRoute()
const { isStudent, isDriver, isAuthenticated, userRole } = useAuth()

const authRoutes = ['/', '/cadastro']
const studentRoutes = ['/enquetes', '/lista-embarque', '/acompanhar-viagem']
const driverRoutes = ['/viagens', '/lista-embarque']
const adminRoutes = ['/admin/estudantes']

const isAdmin = computed(() => {
  const role = (userRole.value || '').toLowerCase()
  return role === 'admin'
})
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl"> <RouterLink to="/">UniBus</RouterLink> </a>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <template v-if="authRoutes.includes(route.path)">
          <li>
            <RouterLink to="/" class="btn mr-2">Login</RouterLink>
          </li>
          <li>
            <RouterLink to="/cadastro" class="btn mr-2">Cadastro</RouterLink>
          </li>
        </template>

        <template v-else-if="isStudent && isAuthenticated">
          <li>
            <RouterLink to="/enquetes" class="btn mr-2">Enquetes</RouterLink>
          </li>
          <li>
            <RouterLink to="/acompanhar-viagem" class="btn mr-2">Acompanhar Viagem</RouterLink>
          </li>
          <li>
            <RouterLink to="/lista-embarque" class="btn mr-2">Lista de embarque</RouterLink>
          </li>
          <li>
            <RouterLink to="/" class="btn mr-2" @click="logout">Sair</RouterLink>
          </li>
        </template>

        <template v-else-if="isDriver && isAuthenticated">
          <li>
            <RouterLink to="/viagens" class="btn mr-2">Viagens</RouterLink>
          </li>
          <li>
            <RouterLink to="/lista-embarque" class="btn mr-2">Lista de embarque</RouterLink>
          </li>
          <li>
            <RouterLink to="/" class="btn mr-2" @click="logout">Sair</RouterLink>
          </li>
        </template>

        <template v-else-if="isAdmin && isAuthenticated">
          <li>
            <RouterLink to="/admin/estudantes" class="btn mr-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 mr-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
              Estudantes
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/" class="btn mr-2" @click="logout">Sair</RouterLink>
          </li>
        </template>

        <template v-else-if="isAuthenticated">
          <li>
            <RouterLink to="/" class="btn mr-2" @click="logout">Sair</RouterLink>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>
