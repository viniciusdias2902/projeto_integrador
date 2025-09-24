<script setup>
import { reactive, computed, onMounted } from 'vue'
import api from '../services/api'

const props = defineProps({
  day: Object,
})

const OPTIONS_MAP = {
  vou_e_volto: 'round_trip',
  apenas_vou: 'one_way_outbound',
  apenas_volto: 'one_way_return',
  nao_vou: 'absent',
}

const LABEL_MAP = {
  vou_e_volto: 'Vou e volto',
  apenas_vou: 'Apenas vou',
  apenas_volto: 'Apenas volto',
  nao_vou: 'Não vou',
}

// Inverte o mapeamento para converter da API para o formato local
const REVERSE_OPTIONS_MAP = Object.fromEntries(
  Object.entries(OPTIONS_MAP).map(([key, value]) => [value, key]),
)

const state = reactive({
  currentVote: null,
  selectedOption: null,
  isLoading: false,
  isSubmitting: false,
})

// Computed para encontrar o voto atual do usuário
const userVote = computed(() => {
  if (!props.day?.votes?.length) return null

  // Aqui você precisaria ter acesso ao ID do usuário atual
  // Por exemplo, através de um store/composable de autenticação
  // const { currentUser } = useAuth()
  // return props.day.votes.find(vote => vote.student.id === currentUser.id)

  // Por enquanto, assumindo que há apenas um voto por enquete por usuário
  // ou que você tem alguma forma de identificar o voto do usuário atual
  return props.day.votes[0] || null
})

// Computed para a opção selecionada baseada no voto existente
const currentSelection = computed({
  get() {
    if (userVote.value) {
      return REVERSE_OPTIONS_MAP[userVote.value.option] || null
    }
    return state.selectedOption
  },
  set(value) {
    state.selectedOption = value
  },
})

// Computed para o texto do badge
const voteStatusText = computed(() => {
  if (userVote.value) {
    const option = REVERSE_OPTIONS_MAP[userVote.value.option]
    return LABEL_MAP[option] || userVote.value.option
  }
  return null
})

onMounted(async () => {
  // Carrega os dados iniciais se necessário
  await loadPollData()
})

async function loadPollData() {
  if (state.isLoading) return

  try {
    state.isLoading = true

    // Carrega os dados atualizados da enquete específica
    const response = await api.get(`polls/${props.day.id}/`)

    // Atualiza os dados da enquete (assumindo que o componente pai pode receber essa atualização)
    // Ou você pode emitir um evento para o componente pai atualizar
    // emit('poll-updated', response.data)
  } catch (err) {
    console.error('Erro ao carregar dados da enquete:', err)
  } finally {
    state.isLoading = false
  }
}

async function submitResponse() {
  const choice = currentSelection.value
  if (!choice || state.isSubmitting) return

  try {
    state.isSubmitting = true

    if (userVote.value) {
      // Atualiza voto existente
      await api.patch(`votes/${userVote.value.id}/`, {
        option: OPTIONS_MAP[choice],
      })
    } else {
      // Cria novo voto
      await api.post('votes/', {
        poll: props.day.id,
        option: OPTIONS_MAP[choice],
      })
    }

    // Recarrega os dados para ter o estado mais atual
    await loadPollData()

    // Reset da seleção local após sucesso
    state.selectedOption = null
  } catch (err) {
    console.error('Erro ao enviar resposta:', err)
    // Aqui você pode adicionar tratamento de erro mais sofisticado
    // Por exemplo, mostrar uma notificação de erro
  } finally {
    state.isSubmitting = false
  }
}

// Função para verificar se houve mudança na seleção
const hasChanges = computed(() => {
  if (!userVote.value && !state.selectedOption) return false
  if (!userVote.value && state.selectedOption) return true
  if (userVote.value && !state.selectedOption) return false

  const currentOption = REVERSE_OPTIONS_MAP[userVote.value.option]
  return currentOption !== state.selectedOption
})
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

    <form class="space-y-3" @submit.prevent="submitResponse">
      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio"
          value="vou_e_volto"
          v-model="currentSelection"
          :disabled="state.isSubmitting"
        />
        <span class="label-text">Vou e volto</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio"
          value="apenas_vou"
          v-model="currentSelection"
          :disabled="state.isSubmitting"
        />
        <span class="label-text">Apenas vou</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio"
          value="apenas_volto"
          v-model="currentSelection"
          :disabled="state.isSubmitting"
        />
        <span class="label-text">Apenas volto</span>
      </label>

      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="radio"
          :name="'day-' + day.id"
          class="radio"
          value="nao_vou"
          v-model="currentSelection"
          :disabled="state.isSubmitting"
        />
        <span class="label-text">Não vou</span>
      </label>

      <!-- Badge responsiva mostrando a opção votada -->
      <div class="mt-4 w-full flex flex-wrap">
        <span class="badge badge-accent break-words w-full sm:w-auto" v-if="voteStatusText">
          Voto computado: {{ voteStatusText }}
        </span>
        <span
          class="badge badge-info break-words w-full sm:w-auto"
          v-else-if="state.selectedOption"
        >
          Selecionado: {{ LABEL_MAP[state.selectedOption] }}
        </span>
      </div>

      <button
        type="submit"
        class="btn btn-success btn-block mt-4"
        :class="{ loading: state.isSubmitting }"
        :disabled="!currentSelection || state.isSubmitting || !hasChanges"
      >
        {{ state.isSubmitting ? 'Enviando...' : 'Enviar resposta' }}
      </button>
    </form>
  </div>
</template>
