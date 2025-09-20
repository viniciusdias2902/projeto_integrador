<template>
  <DefaultLayout>
    <div class="flex flex-wrap justify-center gap-6 my-8">
      <PollComponent
        v-for="day in days"
        :key="day.id"
        :day="day"
        :votedPolls="votedPolls"
        :responses="responses"
      />
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import DefaultLayout from '@/templates/DefaultLayout.vue'

const days = ref([])
const responses = ref({})
const votedPolls = ref(JSON.parse(localStorage.getItem('votedPolls') || '{}'))

onMounted(async () => {
  const { data } = await api.get('polls/')
  days.value = data
})
</script>
