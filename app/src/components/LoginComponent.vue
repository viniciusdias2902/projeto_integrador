<script setup>
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
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
    <div role="alert" class="alert alert-error mt-4" v-if="error">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <span>{{ error }}</span>
    </div>
    <button class="btn btn-neutral mt-4" type="submit" @click="handleLogin">Login</button>
    <button class="btn btn-outline mt-4" @click="$router.push('/cadastro')">Cadastro</button>
  </fieldset>
</template>
