<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const days = ref([])
const responses = ref({})
const votedPolls = ref({})

// Map das opções do radio para os valores da API
const OPTIONS_MAP = {
  vou_e_volto: 'round_trip',
  apenas_vou: 'one_way_outbound',
  apenas_volto: 'one_way_return',
  nao_vou: 'absent',
}

// Recupera polls já votadas do localStorage
const savedVoted = JSON.parse(localStorage.getItem('votedPolls') || '{}')
votedPolls.value = savedVoted

onMounted(async () => {
  try {
    const { data } = await api.get('polls/')
    days.value = data
  } catch (err) {
    console.error('Erro ao buscar polls:', err)
  }
})

async function submitResponse(dayId) {
  const choice = responses.value[dayId]
  if (!choice) return

  try {
    await api.post('votes/create/', {
      poll: dayId,
      option: OPTIONS_MAP[choice],
    })

    // Salva que já votou
    votedPolls.value[dayId] = true
    localStorage.setItem('votedPolls', JSON.stringify(votedPolls.value))
  } catch (err) {
    console.error('Erro ao enviar resposta:', err)
  }
}
</script>

<template>
  <div class="space-y-6">
    <div
      v-for="day in days"
      :key="day.id"
      class="max-w-md mx-auto bg-base-100 shadow-md rounded-box p-6 mb-4 lg:w-96 w-60"
    >
      <h2 class="text-xl font-bold mb-4">
        {{
          new Date(day.date).toLocaleDateString('pt-BR', {
            weekday: 'long',
            day: '2-digit',
            month: '2-digit',
          })
        }}
      </h2>

      <form class="space-y-3" @submit.prevent="submitResponse(day.id)">
        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="radio"
            :name="'day-' + day.id"
            class="radio checked"
            value="vou_e_volto"
            v-model="responses[day.id]"
          />
          <span class="label-text">Vou e volto</span>
        </label>

        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="radio"
            :name="'day-' + day.id"
            class="radio checked"
            value="apenas_vou"
            v-model="responses[day.id]"
          />
          <span class="label-text">Apenas vou</span>
        </label>

        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="radio"
            :name="'day-' + day.id"
            class="radio checked"
            value="apenas_volto"
            v-model="responses[day.id]"
          />
          <span class="label-text">Apenas volto</span>
        </label>

        <label class="flex items-center gap-3 cursor-pointer">
          <input
            type="radio"
            :name="'day-' + day.id"
            class="radio checked"
            value="nao_vou"
            v-model="responses[day.id]"
          />
          <span class="label-text">Não vou</span>
        </label>
        <span class="badge badge-accent mt-4" v-if="votedPolls[day.id]"
          >Você já votou nessa enquete</span
        >
        <button type="submit" class="btn btn-success btn-block mt-4">Enviar resposta</button>
      </form>
    </div>
  </div>
</template>
