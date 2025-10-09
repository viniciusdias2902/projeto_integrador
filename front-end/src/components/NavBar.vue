<script setup>
import { useRoute } from 'vue-router'
import { logout } from '@/services/auth'
const route = useRoute()
const authRoutes = ['/', '/cadastro']
const appRoutes = ['/enquetes', '/lista-embarque']
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

        <template v-else-if="appRoutes.includes(route.path)">
          <li>
            <RouterLink to="/enquetes" class="btn mr-2">Enquetes</RouterLink>
          </li>
          <li>
            <RouterLink to="/lista-embarque" class="btn mr-2">Lista de embarque</RouterLink>
          </li>
          <li>
            <RouterLink to="/" class="btn mr-2" @click="logout">Sair</RouterLink>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>
