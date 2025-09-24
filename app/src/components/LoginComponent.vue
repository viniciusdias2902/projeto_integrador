<script setup>
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
import AlertComponent from './AlertComponent.vue'
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref(null)

async function handleLogin() {
  try {
    await login(email.value, password.value)
    router.push('/enquetes')
  } catch (err) {
    error.value = 'Email ou senha inválidos'
  }
}
</script>

<template>
  <fieldset
    class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4"
    @submit.prevent
  >
    <legend class="fieldset-legend">Login</legend>

    <label class="label">Email</label>
    <input type="email" class="input" placeholder="Email" v-model="email" />

    <label class="label">Senha</label>
    <input type="password" class="input" placeholder="Senha" v-model="password" />
    <AlertComponent v-if="error">{{ error }}</AlertComponent>
    <button class="btn btn-neutral mt-4" type="submit" @click="handleLogin">Login</button>
    <button class="btn btn-outline mt-4" @click="$router.push('/cadastro')">Cadastro</button>
  </fieldset>
</template>
