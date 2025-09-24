<script setup>
const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`
import { verifyAndRefreshToken, verifyToken } from '@/services/auth'

const polls = ref([])

async function getPolls() {
  let isValid = verifyAndRefreshToken()
  if (isValid) {
    const response = await fetch(POLLS_URL, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
    })
    const data = await response.json()
    polls.value = data
    if (!response.ok) {
      throw new Error('Erro')
    }
    console.log(polls.value)
  }
}
onMounted(() => getPolls())
import DefaultLayout from '@/templates/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <p>Refactoring</p>
  </DefaultLayout>
</template>

<!-- <template>
  <DefaultLayout>
    <div class="flex flex-wrap justify-center gap-6 my-8">
      <div v-if="isLoading" class="text-center w-full">
        <div class="loading loading-spinner loading-lg"></div>
        <p class="mt-4">Carregando enquetes...</p>
      </div>

      <PollComponent
        v-else
        v-for="day in days"
        :key="day.id"
        :day="day"
        @update-poll="updatePollData"
      />
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import PollComponent from '@/components/PollComponent.vue'

const days = ref([])
const isLoading = ref(false)

onMounted(async () => {
  await loadPolls()
})

async function loadPolls() {
  try {
    isLoading.value = true
    const { data } = await api.get('polls/')
    days.value = data
  } catch (error) {
    console.error('Erro ao carregar enquetes:', error)
    // Aqui você pode adicionar tratamento de erro, como mostrar uma notificação
  } finally {
    isLoading.value = false
  }
}

function updatePollData(updatedPoll) {
  // Encontra e atualiza a enquete específica no array
  const index = days.value.findIndex((day) => day.id === updatedPoll.id)
  if (index !== -1) {
    days.value[index] = updatedPoll
  }
}
</script> -->
