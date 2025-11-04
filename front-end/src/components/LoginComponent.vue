<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../services/auth'
import { useAuth } from '@/useAuth'

const router = useRouter()
const { updateRole, isStudent, isDriver, userRole } = useAuth()

const email = ref('')
const password = ref('')
const error = ref(null)

async function handleLogin() {
  error.value = null
  try {
    const response = await login(email.value, password.value)

    console.log('Login response:', response)
    console.log('Role from response:', response.role)

    updateRole()

    console.log('User role after update:', userRole.value)
    console.log('Is student:', isStudent.value)
    console.log('Is driver:', isDriver.value)

    const normalizedRole = (response.role || '').toLowerCase()

    if (normalizedRole === 'student') {
      console.log('Redirecting to /enquetes')
      router.push('/enquetes')
    } else if (normalizedRole === 'driver') {
      console.log('Redirecting to /viagens')
      router.push('/viagens')
    } else if (normalizedRole === 'admin') {
      console.log('Redirecting to /admin/estudantes')
      router.push('/admin/estudantes')
    } else {
      console.log('Unknown role, redirecting to /enquetes. Role:', response.role)
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
