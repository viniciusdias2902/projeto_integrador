<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <InputField id="name" label="Nome" v-model="form.name" />
    <InputField id="email" label="E-mail" type="email" v-model="form.email" />
    <InputField id="password" label="Senha" type="password" v-model="form.password" />
    <InputField id="phone" label="Telefone" v-model="form.phone" />

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

    <p v-if="sucessMessage" class="mt-4 text-green-600 text-center">
      {{ sucessMessage }}
    </p>
    <p v-if="errorMessage" class="mt-4 text-red-600 text-center">{{ errorMessage }}</p>
  </form>
</template>

<script>
import InputField from './InputField.vue'
import SelectField from './SelectField.vue'

export default {
  name: 'StudentForm',
  components: {
    InputField,
    SelectField,
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
      },
      sucessMessage: '',
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
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://localhost:8000/api/v1/students/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form),
        })

        if (!response.ok) throw new Error('Erro ao cadastrar aluno')

        this.sucessMessage = 'Cadastro realizado com sucesso!'
        this.errorMessage = ''
        this.form = {
          name: '',
          email: '',
          password: '',
          phone: '',
          university: '',
          class_shift: '',
        }
      } catch (error) {
        console.error(error)
        this.errorMessage = 'Erro ao cadastrar aluno. Tente novamente.'
        this.sucessMessage = ''
      }
    },
  },
}
</script>
