<script setup>
import {ref, onMounted} from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import RegisterLayout from '@/templates/RegisterLayout.vue'
import StudentForm from '@/components/StudentForm.vue'

const BOARDING_POINTS_URL = ${import.meta.env.VITE_APP_API_URL}boarding-points/

const boardingPoints = ref([])

async function getBoardingPoints() {
  let isValid = verifyAndRefreshToken()
  if (isValid) {
    const response = await fetch(BOARDING_POINTS_URL, {
      headers: { Authorization: Bearer ${localStorage.getItem('access')} },
    })
    const data = await response.json()
    boardingPoints.value = data
    if (!response.ok) {
      throw new Error('Erro')
    }
    console.log(boardingPoints.value)
  }
}
</script>

<template>
  <RegisterLayout>
    <div class="w-full max-w-3xl p-6 bg-gray-100 rounded-xl shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-6">Cadastro de Alunos</h2>
      <StudentForm />
    </div>
  </RegisterLayout>
</template>
