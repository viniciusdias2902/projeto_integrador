<script setup>
import api from '../services/api'

defineProps({
  day: Object,
  votedPolls: Object,
  responses: Object,
})

async function submitResponse(dayId) {
  const choice = responses[dayId]
  if (!choice) return

  try {
    await api.post('votes/create/', {
      poll: dayId,
      option: {
        vou_e_volto: 'round_trip',
        apenas_vou: 'one_way_outbound',
        apenas_volto: 'one_way_return',
        nao_vou: 'absent',
      }[choice],
    })
    votedPolls[dayId] = true
    localStorage.setItem('votedPolls', JSON.stringify(votedPolls))
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div class="max-w-md bg-base-100 shadow-md rounded-box p-6 mb-4 lg:w-96 w-60">
    <h2 class="text-xl font-bold mb-4">
      {{
        (() => {
          const dateStr = new Date(day.date).toLocaleDateString('pt-BR', {
            weekday: 'long',
            day: '2-digit',
            month: '2-digit',
          })
          return dateStr.charAt(0).toUpperCase() + dateStr.slice(1)
        })()
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
      <span class="badge badge-accent mt-4" v-if="votedPolls[day.id]">Voto computado</span>
      <button type="submit" class="btn btn-success btn-block mt-4">Enviar resposta</button>
    </form>
  </div>
</template>
