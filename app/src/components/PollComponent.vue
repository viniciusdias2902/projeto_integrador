<script setup>
import { reactive } from 'vue'
import api from '../services/api'

// Props (somente leitura)
const props = defineProps({
  day: Object,
  votedPolls: Object, // { [dayId]: { voteId, option } }
  responses: Object,
})

// Criar uma cópia reativa local
const localResponses = reactive({ ...props.responses })

// Map das opções do radio para os valores da API
const OPTIONS_MAP = {
  vou_e_volto: 'round_trip',
  apenas_vou: 'one_way_outbound',
  apenas_volto: 'one_way_return',
  nao_vou: 'absent',
}

// Inverter o map para mostrar a label
const LABEL_MAP = {
  vou_e_volto: 'Vou e volto',
  apenas_vou: 'Apenas vou',
  apenas_volto: 'Apenas volto',
  nao_vou: 'Não vou',
}

async function submitResponse(dayId) {
  const choice = localResponses[dayId]
  if (!choice) return

  try {
    if (props.votedPolls[dayId]?.voteId) {
      // Atualiza voto existente
      await api.patch(`votes/${props.votedPolls[dayId].voteId}/update/`, {
        option: OPTIONS_MAP[choice],
      })
      props.votedPolls[dayId].option = choice
    } else {
      // Cria novo voto
      const response = await api.post('votes/create/', {
        poll: dayId,
        option: OPTIONS_MAP[choice],
      })
      props.votedPolls[dayId] = {
        voteId: response.data.id,
        option: choice,
      }
      localStorage.setItem('votedPolls', JSON.stringify(props.votedPolls))
    }

    // Mantém o radio selecionado
    localResponses[dayId] = choice
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

      <!-- Badge mostrando a opção votada -->
      <span class="badge badge-accent mt-4" v-if="votedPolls[day.id]">
        Voto computado: {{ LABEL_MAP[votedPolls[day.id].option] }}
      </span>

      <button type="submit" class="btn btn-success btn-block mt-4">Enviar resposta</button>
    </form>
  </div>
</template>
