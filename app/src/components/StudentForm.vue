<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div>
      <InputField id="name" label="Nome" v-model="form.name" />
      <ValidationMessage :message="errors.name" />
    </div>

    <div>
      <InputField id="email" label="E-mail" type="email" v-model="form.email" />
      <ValidationMessage :message="errors.email" />
    </div>

    <div>
      <InputField id="password" label="Senha" type="password" v-model="form.password" />
      <ValidationMessage :message="errors.password" />
    </div>

    <div>
      <InputField id="phone" label="Telefone" v-model="form.phone" />
      <ValidationMessage :message="errors.phone" />
    </div>
    <div>
      <SelectField
        id="boarding_point"
        label="Ponto de Embarque"
        :options="boardingPoints"
        v-model="form.boarding_point"
      />
    </div>
    <SelectField
      id="university"
      label="Universidade"
      :options="universities"
      v-model="form.university"
    />

    <SelectField id="class_shift" label="Turno" :options="shifts" v-model="form.class_shift" />

    <button type="submit" class="btn bg-black text-white hover:bg-gray-800 w-full">
      Cadastrar
    </button>

    <p v-if="successMessage" class="mt-4 text-green-600 text-center">
      {{ successMessage }}
    </p>
    <p v-if="errorMessage" class="mt-4 text-red-600 text-center">{{ errorMessage }}</p>
  </form>
</template>

<script>
import InputField from './InputField.vue'
import SelectField from './SelectField.vue'
import ValidationMessage from './ValidationMessage.vue'

export default {
  name: 'StudentForm',
  components: {
    InputField,
    SelectField,
    ValidationMessage,
  },
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        phone: '',
        university: '',
        class_shift: '',
        boarding_point: 1,
      },
      errors: {
        name: '',
        email: '',
        password: '',
        phone: '',
      },
      successMessage: '',
      errorMessage: '',
      universities: [
        { value: 'UESPI', label: 'UESPI' },
        { value: 'IFPI', label: 'IFPI' },
        { value: 'CHRISFAPI', label: 'CHRISFAPI' },
      ],
      shifts: [
        { value: 'M', label: 'Manhã' },
        { value: 'A', label: 'Tarde' },
        { value: 'E', label: 'Noite' },
        { value: 'M-A', label: 'Manhã e Tarde' },
        { value: 'A-E', label: 'Tarde e Noite' },
      ],
      boardingPoints: [
        { value: 1, label: 'Ponto 1' },
        { value: 2, label: 'Ponto 2' },
        { value: 3, label: 'Ponto 3' },
      ],
    }
  },
  methods: {
    clearErrors() {
      this.errors = {
        name: '',
        email: '',
        password: '',
        phone: '',
      }
    },
    resetForm() {
      this.form = {
        name: '',
        email: '',
        password: '',
        phone: '',
        university: '',
        class_shift: '',
        boarding_point: 1,
      }
      this.clearErrors()
      this.errorMessage = ''
    },
    validateForm() {
      let valid = true

      this.clearErrors()

      if (!this.form.name || this.form.name.length < 3) {
        this.errors.name = 'Nome deve ter pelo menos 3 caracteres.'
        valid = false
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.form.email || !emailRegex.test(this.form.email)) {
        this.errors.email = 'Insira um e-mail válido.'
        valid = false
      }

      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/
      if (!this.form.password || !passwordRegex.test(this.form.password)) {
        this.errors.password = 'A senha deve conter pelo menos 8 caracteres, uma letra e um número.'
        valid = false
      }

      const phoneDigits = this.form.phone.replace(/\D/g, '')
      if (!phoneDigits || phoneDigits.length < 10 || phoneDigits.length > 11) {
        this.errors.phone = 'Telefone deve conter 10 ou 11 números.'
        valid = false
      }

      return valid
    },
    async submitForm() {
      if (!this.validateForm()) return

      try {
        const response = await fetch('http://localhost:8000/api/v1/students/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form),
        })

        const result = await response.json()

        if (!response.ok) {
          if (result.email && Array.isArray(result.email)) {
            const message = result.email[0]
            if (message === 'This email is already in use') {
              this.errors.email = 'Esse email já está sendo usado por outro usuário.'
            } else {
              this.errors.email = message
            }
          }
          throw new Error('Erro ao cadastrar')
        }

        this.successMessage = 'Cadastro realizado com sucesso!'
        this.resetForm()
      } catch (error) {
        console.error(error)
        if (!this.errors.email) {
          this.errorMessage = 'Erro ao cadastrar aluno. Tente novamente.'
        }
        this.successMessage = ''
      }
    },
  },
}
</script>
