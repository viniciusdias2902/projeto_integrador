<script setup>
import { reactive, onMounted } from 'vue'
import api from '../services/api'

// Props (somente leitura)
const props = defineProps({
  day: Object,
  votedPolls: Object, // { [dayId]: { voteId, option } }
  responses: Object,
})

// Map das opções do radio para os valores da API
const OPTIONS_MAP = {
  vou_e_volto: 'round_trip',
  apenas_vou: 'one_way_outbound',
  apenas_volto: 'one_way_return',
  nao_vou: 'absent',
}

// Map para exibir a label legível
const LABEL_MAP = {
  vou_e_volto: 'Vou e volto',
  apenas_vou: 'Apenas vou',
  apenas_volto: 'Apenas volto',
  nao_vou: 'Não vou',
}

// Criar uma cópia reativa local
const localResponses = reactive({})

// Inicializa votedPolls e localResponses a partir do localStorage
onMounted(() => {
  const storedVotes = localStorage.getItem('votedPolls')
  if (storedVotes) {
    const parsed = JSON.parse(storedVotes)
    Object.assign(props.votedPolls, parsed)
    for (const dayId in parsed) {
      localResponses[dayId] = parsed[dayId].option
    }
  }
})

async function submitResponse(dayId) {
  const choice = localResponses[dayId]
  if (!choice) return

  try {
    if (props.votedPolls[dayId]?.voteId) {
      await api.patch(`votes/${props.votedPolls[dayId].voteId}/update/`, {
        option: OPTIONS_MAP[choice],
      })
      props.votedPolls[dayId].option = choice
    } else {
      const response = await api.post('votes/create/', {
        poll: dayId,
        option: OPTIONS_MAP[choice],
      })
      props.votedPolls[dayId] = {
        voteId: response.data.id,
        option: choice,
      }
    }

    // Atualiza o localStorage
    localStorage.setItem('votedPolls', JSON.stringify(props.votedPolls))
    localResponses[dayId] = choice
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div class="w-full max-w-md sm:max-w-md bg-base-100 shadow-md rounded-box p-6 mb-4">
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
          v-model="localResponses[day.id]"
        />
        <span class="label-text">Vou e volto</span>
      </label>
      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio checked"
          value="apenas_vou"
          v-model="localResponses[day.id]"
        />
        <span class="label-text">Apenas vou</span>
      </label>
      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio checked"
          value="apenas_volto"
          v-model="localResponses[day.id]"
        />
        <span class="label-text">Apenas volto</span>
      </label>
      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio checked"
          value="nao_vou"
          v-model="localResponses[day.id]"
        />
        <span class="label-text">Não vou</span>
      </label>

      <!-- Badge responsiva mostrando a opção votada -->
      <div class="mt-4 w-full flex flex-wrap">
        <span class="badge badge-accent break-words w-full sm:w-auto" v-if="votedPolls[day.id]">
          Voto computado: {{ LABEL_MAP[votedPolls[day.id].option] }}
        </span>
      </div>

      <button type="submit" class="btn btn-success btn-block mt-4">Enviar resposta</button>
    </form>
  </div>
</template>
