<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
import { useAuth } from '@/useAuth'

const router = useRouter()
const { updateRole, isStudent, isDriver } = useAuth()

const email = ref('')
const password = ref('')
const error = ref(null)

async function handleLogin() {
  error.value = null
  try {
    await login(email.value, password.value)

    updateRole()

    if (isStudent.value) {
      router.push('/enquetes')
    } else if (isDriver.value) {
      router.push('/viagens')
    } else {
      router.push('/enquetes')
    }
  } catch (err) {
    error.value = 'Email ou senha inválidos'
    console.error('Erro no login:', err)
  }
}
</script>

<template>
  <FieldsetComponent title="Login">
    <LabelComponent for="email">Email</LabelComponent>
    <input type="email" class="input" placeholder="Email" v-model="email" id="email" />
    <LabelComponent for="password">Senha</LabelComponent>
    <input type="password" class="input" placeholder="Senha" v-model="password" id="password" />
    <AlertComponent v-if="error" class="mt-4">{{ error }}</AlertComponent>
    <ButtonNeutral @click="handleLogin" class="mt-4">Login</ButtonNeutral>
    <OutlineButton @click="router.push('/cadastro')">Cadastro</OutlineButton>
  </FieldsetComponent>
</template>
