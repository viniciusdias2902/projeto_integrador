<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-[500px] p-6 bg-gray-100 rounded-xl shadow-lg">
      <h2 class="text-2xl font-bold text-center mb-6">Cadastro de Alunos</h2>
      <StudentForm />
    </div>
  </div>
</template>

<script>
import StudentForm from '../components/StudentForm.vue'

export default {
  name: 'RegistrationPage',
  components: {
    StudentForm,
  },
}
</script>
