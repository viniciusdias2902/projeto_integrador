<script setup>
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
import AlertComponent from './AlertComponent.vue'
import OutlineButton from './OutlineButton.vue'
import FieldsetComponent from './FieldsetComponent.vue'
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
  <FieldsetComponent title="Login">
    <label class="label" for="email">Email</label>
    <input type="email" class="input" placeholder="Email" v-model="email" id="email" />

    <label class="label">Senha</label>
    <input type="password" class="input" placeholder="Senha" v-model="password" />
    <AlertComponent v-if="error" class="mt-4">{{ error }}</AlertComponent>
    <ButtonNeutral @click="handleLogin" class="mt-4">Login</ButtonNeutral>
    <OutlineButton @click="router.push('/cadastro')">Cadastro</OutlineButton>
  </FieldsetComponent>
</template>
