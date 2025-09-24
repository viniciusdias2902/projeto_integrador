<script setup>
const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`
import PollComponent from '@/components/PollComponent.vue'
import { verifyAndRefreshToken, decodeJwt } from '@/services/auth'
const token = localStorage.getItem('access')
const decoded = decodeJwt(token)
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
    console.log(decoded.user_id)
  }
}

function getDiaSemana(dateString) {
  const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
  const date = new Date(dateString)
  return diasSemana[date.getDay()]
}

onMounted(() => getPolls())
import DefaultLayout from '@/templates/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <div class="flex gap-4 flex-wrap justify-center mb-4">
      <PollComponent
        v-for="poll in polls"
        :day="getDiaSemana(poll.date)"
        :key="poll.id"
        :name="poll.id"
      ></PollComponent>
    </div>
  </DefaultLayout>
</template>
