<script setup>
import { ref, onMounted } from 'vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const form = ref({
  name: '',
  email: '',
  password: '',
  phone: '',
  university: '',
  class_shift: '',
  boarding_point: null,
})

const errors = ref({
  name: '',
  email: '',
  password: '',
  phone: '',
})

const successMessage = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const isLoadingPoints = ref(true)

const universities = [
  { value: 'UESPI', label: 'Universidade Estadual do Piauí' },
  { value: 'CHRISFAPI', label: 'Christus Faculdade do Piauí' },
  { value: 'IFPI', label: 'Instituto Federal do Piauí' },
  { value: 'ETC', label: 'Outro' },
]

const shifts = [
  { value: 'M', label: 'Manhã' },
  { value: 'A', label: 'Tarde' },
  { value: 'E', label: 'Noite' },
  { value: 'M-A', label: 'Manhã e Tarde' },
  { value: 'A-E', label: 'Tarde e Noite' },
]

const boardingPoints = ref([])

async function fetchBoardingPoints() {
  isLoadingPoints.value = true
  try {
    const response = await fetch(`${API_BASE_URL}boarding-points/`)
    
    if (!response.ok) {
      throw new Error('Erro ao carregar pontos de embarque')
    }
    
    const data = await response.json()
    boardingPoints.value = data.map(point => ({
      value: point.id,
      label: point.name
    }))
    
    if (boardingPoints.value.length > 0) {
      form.value.boarding_point = boardingPoints.value[0].value
    }
  } catch (error) {
    console.error('Error fetching boarding points:', error)
    errorMessage.value = 'Erro ao carregar pontos de embarque'
  } finally {
    isLoadingPoints.value = false
  }
}

function clearErrors() {
  errors.value = {
    name: '',
    email: '',
    password: '',
    phone: '',
  }
}

function resetForm() {
  form.value = {
    name: '',
    email: '',
    password: '',
    phone: '',
    university: '',
    class_shift: '',
    boarding_point: boardingPoints.value.length > 0 ? boardingPoints.value[0].value : null,
  }
  clearErrors()
  errorMessage.value = ''
}

function validateForm() {
  let valid = true
  clearErrors()

  if (!form.value.name || form.value.name.length < 3) {
    errors.value.name = 'Nome deve ter pelo menos 3 caracteres.'
    valid = false
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.value.email || !emailRegex.test(form.value.email)) {
    errors.value.email = 'Insira um e-mail válido.'
    valid = false
  }

  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/
  if (!form.value.password || !passwordRegex.test(form.value.password)) {
    errors.value.password = 'A senha deve conter pelo menos 8 caracteres, uma letra e um número.'
    valid = false
  }

  const phoneDigits = form.value.phone.replace(/\D/g, '')
  if (!phoneDigits || phoneDigits.length < 10 || phoneDigits.length > 11) {
    errors.value.phone = 'Telefone deve conter 10 ou 11 números.'
    valid = false
  }

  if (!form.value.university) {
    errorMessage.value = 'Selecione uma universidade.'
    valid = false
  }

  if (!form.value.class_shift) {
    errorMessage.value = 'Selecione um turno.'
    valid = false
  }

  if (!form.value.boarding_point) {
    errorMessage.value = 'Selecione um ponto de embarque.'
    valid = false
  }

  return valid
}

function translateBackendError(errorField, errorMessage) {
  const translations = {
    email: {
      'This email is already in use': 'Este email já está em uso',
      'user with this email already exists.': 'Usuário com este email já existe.',
      'Enter a valid email address.': 'Insira um endereço de email válido.'
    },
    phone: {
      'user with this phone already exists.': 'Usuário com este telefone já existe.',
      'Enter a valid phone number.': 'Insira um número de telefone válido.'
    },
    password: {
      'This password is too short. It must contain at least 8 characters.': 'Esta senha é muito curta. Deve conter pelo menos 8 caracteres.',
      'This password is too common.': 'Esta senha é muito comum.',
      'This password is entirely numeric.': 'Esta senha é inteiramente numérica.'
    },
    name: {
      'This field may not be blank.': 'Este campo não pode estar vazio.'
    }
  }

  if (translations[errorField] && translations[errorField][errorMessage]) {
    return translations[errorField][errorMessage]
  }

  return errorMessage
}

async function submitForm() {
  if (!validateForm()) return

  isLoading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}students/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value),
    })

    const result = await response.json()

    if (!response.ok) {
      if (result.email && Array.isArray(result.email)) {
        const message = result.email[0]
        errors.value.email = translateBackendError('email', message)
      } else if (result.phone && Array.isArray(result.phone)) {
        const message = result.phone[0]
        errors.value.phone = translateBackendError('phone', message)
      } else if (result.password && Array.isArray(result.password)) {
        const message = result.password[0]
        errors.value.password = translateBackendError('password', message)
      } else if (result.name && Array.isArray(result.name)) {
        const message = result.name[0]
        errors.value.name = translateBackendError('name', message)
      } else {
        errorMessage.value = result.detail || 'Erro ao cadastrar aluno. Tente novamente.'
      }
      throw new Error('Erro ao cadastrar')
    }

    successMessage.value = 'Cadastro realizado com sucesso! Você já pode fazer login.'
    resetForm()
    
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
  } catch (error) {
    console.error('Submit error:', error)
    if (!errors.value.email && !errorMessage.value) {
      errorMessage.value = 'Erro ao cadastrar aluno. Tente novamente.'
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchBoardingPoints()
})
</script>

<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div>
      <InputField 
        id="name" 
        label="Nome Completo" 
        v-model="form.name"
        placeholder="Ex: João da Silva"
        :disabled="isLoading"
      />
      <ValidationMessage :message="errors.name" />
    </div>

    <div>
      <InputField 
        id="email" 
        label="E-mail" 
        type="email" 
        v-model="form.email"
        placeholder="seu.email@exemplo.com"
        :disabled="isLoading"
      />
      <ValidationMessage :message="errors.email" />
    </div>

    <div>
      <InputField 
        id="password" 
        label="Senha" 
        type="password" 
        v-model="form.password"
        placeholder="Mínimo 8 caracteres, 1 letra e 1 número"
        :disabled="isLoading"
      />
      <ValidationMessage :message="errors.password" />
    </div>

    <div>
      <InputField 
        id="phone" 
        label="Telefone" 
        v-model="form.phone"
        placeholder="(00) 00000-0000"
        :disabled="isLoading"
      />
      <ValidationMessage :message="errors.phone" />
    </div>

    <div>
      <SelectField
        id="university"
        label="Universidade"
        :options="universities"
        v-model="form.university"
        :disabled="isLoading"
      />
    </div>

    <div>
      <SelectField 
        id="class_shift" 
        label="Turno" 
        :options="shifts" 
        v-model="form.class_shift"
        :disabled="isLoading"
      />
    </div>

    <div>
      <SelectField
        id="boarding_point"
        label="Ponto de Embarque"
        :options="boardingPoints"
        v-model="form.boarding_point"
        :disabled="isLoading || isLoadingPoints"
      />
      <p v-if="isLoadingPoints" class="text-sm text-base-content/60 mt-1">
        Carregando pontos de embarque...
      </p>
    </div>

    <button 
      type="submit" 
      class="btn btn-primary w-full"
      :disabled="isLoading || isLoadingPoints"
    >
      <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
      <span>{{ isLoading ? 'Cadastrando...' : 'Cadastrar' }}</span>
    </button>

    <div v-if="successMessage" class="alert alert-success">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ successMessage }}</span>
    </div>

    <div v-if="errorMessage" class="alert alert-error">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ errorMessage }}</span>
    </div>
  </form>
</template>