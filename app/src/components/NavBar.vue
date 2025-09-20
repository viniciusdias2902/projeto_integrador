<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const authRoutes = ['/']
const appRoutes = ['/enquetes', '/lista-embarque']
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl">UniBus</a>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <!-- Grupo de autenticação -->
        <template v-if="authRoutes.includes(route.path)">
          <li>
            <RouterLink to="/" class="btn mr-2">Login</RouterLink>
          </li>
          <li>
            <RouterLink to="/cadastro" class="btn mr-2">Cadastro</RouterLink>
          </li>
        </template>

        <!-- Grupo de app -->
        <template v-else-if="appRoutes.includes(route.path)">
          <li>
            <RouterLink to="/enquetes" class="btn mr-2">Enquetes</RouterLink>
          </li>
          <li>
            <RouterLink to="/lista-embarque" class="btn mr-2">Lista de embarque</RouterLink>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>
