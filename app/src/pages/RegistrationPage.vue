<script setup>
import RegisterLayout from '@/templates/RegisterLayout.vue'
import StudentForm from '@/components/StudentForm.vue'
</script>

<template>
  <RegisterLayout>
    <div class="w-full max-w-3xl p-6 bg-gray-100 rounded-xl shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-6">Cadastro de Alunos</h2>
      <StudentForm />
    </div>
  </RegisterLayout>
</template>
