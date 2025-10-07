<script setup>
const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`
import PollComponent from '@/components/PollComponent.vue'
import { verifyAndRefreshToken } from '@/services/auth'
import { ref, onMounted } from 'vue';

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
    console.log(polls.value[0].date)
  }
}

function getDiaSemana(dateString) {
  const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
  const date = new Date(`${dateString}T00:00:00`);
  return diasSemana[date.getDay()];
}

onMounted(() => getPolls())
import DefaultLayout from '@/templates/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <div class="flex flex-wrap gap-4 items-center justify-center max-w-200 mb-4g">
      <PollComponent
        v-for="poll in polls"
        :day="getDiaSemana(poll.date)"
        :key="poll.id"
        :name="poll.id"
      />
    </div>
  </DefaultLayout>
</template>
