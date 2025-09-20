<script setup>
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref(null)

async function handleLogin() {
  try {
    console.log(email.value)
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

    <button class="btn btn-neutral mt-4" type="submit" @click="handleLogin">Login</button>
    <button class="btn btn-outline mt-4">Cadastro</button>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </fieldset>
</template>
