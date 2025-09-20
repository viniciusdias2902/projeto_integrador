<script setup>
import { login } from '../services/auth'

const email = ref('')
const password = ref('')
const error = ref(null)

async function handleLogin(e) {
  e.preventDefault()
  try {
    await login(email.value, password.value)
    alert('Login feito com sucesso!')
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
    <input type="email" class="input" placeholder="Email" />

    <label class="label">Senha</label>
    <input type="password" class="input" placeholder="Senha" />

    <button class="btn btn-neutral mt-4" type="submit" @click="handleLogin">Login</button>
    <button class="btn btn-outline mt-4">Cadastro</button>
  </fieldset>
</template>
