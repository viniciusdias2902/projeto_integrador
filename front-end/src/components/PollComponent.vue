<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'

const props = defineProps({ 
  name: [String, Number], 
  day: String,
  date: String // Adicionando a data completa para validação
})

const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`
const VOTES_URL = `${import.meta.env.VITE_APP_API_URL}votes/`

const selectedOption = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const existingVoteId = ref(null)

const token = localStorage.getItem('access')

// Função para verificar se pode votar em uma opção específica
function canVoteForOption(option) {
  if (!props.date) return true
  
  const now = new Date()
  const pollDate = new Date(`${props.date}T00:00:00`)
  
  // Se a enquete não é para hoje, permite votar
  if (now.toDateString() !== pollDate.toDateString()) {
    if (now > pollDate) return false // Enquete já passou
    return true // Enquete futura
  }
  
  // Se é o dia da enquete, verifica o horário
  const currentHour = now.getHours()
  
  if (option === 'round_trip' || option === 'one_way_outbound') {
    // Limite até 12:00
    return currentHour < 12
  } else if (option === 'one_way_return' || option === 'absent') {
    // Limite até 18:00
    return currentHour < 18
  }
  
  return false
}

// Computed para verificar se pode votar na opção selecionada
const canVoteInSelectedOption = computed(() => {
  if (!selectedOption.value) return true
  return canVoteForOption(selectedOption.value)
})

// Mensagem de aviso sobre horários
const timeWarning = computed(() => {
  if (!props.date) return ''
  
  const now = new Date()
  const pollDate = new Date(`${props.date}T00:00:00`)
  
  // Se não é hoje, não mostra aviso
  if (now.toDateString() !== pollDate.toDateString()) {
    if (now > pollDate) return 'Esta enquete já foi encerrada'
    return ''
  }
  
  const currentHour = now.getHours()
  
  if (currentHour < 12) {
    return '⏰ Todas as opções disponíveis até 12h (ida/volta) e 18h (volta/ausente)'
  } else if (currentHour < 18) {
    return '⏰ Apenas "Apenas volta" e "Não vou" disponíveis até 18h'
  } else {
    return '❌ Prazo de votação encerrado para hoje'
  }
})

// Verificar se opção está desabilitada
function isOptionDisabled(option) {
  return !canVoteForOption(option)
}

// Obter mensagem de tooltip para opções desabilitadas
function getDisabledTooltip(option) {
  if (option === 'round_trip' || option === 'one_way_outbound') {
    return 'Disponível apenas até 12:00'
  }
  return 'Disponível apenas até 18:00'
}

function getUserIdFromDecodedToken() {
  try {
    const payload = token.split('.')[1]
    const decoded = JSON.parse(atob(payload))
    return decoded.user_id || decoded.id || null
  } catch {
    return null
  }
}

const userId = token ? getUserIdFromDecodedToken() : null

async function fetchPoll() {
  verifyAndRefreshToken()
  errorMessage.value = ''
  isLoading.value = true
  
  try {
    const response = await fetch(`${POLLS_URL}${props.name}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to fetch poll')
    }

    const poll = await response.json()
    const userVote = poll.votes.find((vote) => Number(vote.student.id) === Number(userId))

    if (userVote) {
      existingVoteId.value = userVote.id
      selectedOption.value = userVote.option
      successMessage.value = 'Você já votou nesta enquete'
    }
  } catch (error) {
    console.error('Fetch poll error:', error)
    errorMessage.value = error.message || 'Falha ao carregar a enquete. Tente atualizar a página.'
  } finally {
    isLoading.value = false
  }
}

async function submitVote() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!selectedOption.value) {
    errorMessage.value = 'Selecione uma opção antes de enviar'
    return
  }

  // Validar horário antes de enviar
  if (!canVoteInSelectedOption.value) {
    const option = selectedOption.value
    if (option === 'round_trip' || option === 'one_way_outbound') {
      errorMessage.value = 'O prazo para votar em "Ida e Volta" ou "Apenas Ida" é até 12:00'
    } else {
      errorMessage.value = 'O prazo para votar em "Apenas Volta" ou "Não Vou" é até 18:00'
    }
    return
  }

  isLoading.value = true

  try {
    let response

    if (existingVoteId.value) {
      // Atualizar voto existente
      response = await fetch(`${VOTES_URL}${existingVoteId.value}/update/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ option: selectedOption.value }),
      })
    } else {
      // Criar novo voto
      response = await fetch(`${VOTES_URL}create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          poll: Number(props.name),
          option: selectedOption.value,
        }),
      })
    }

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to submit vote')
    }

    const data = await response.json()
    console.log('Vote submitted:', data)

    successMessage.value = existingVoteId.value ? 'Voto atualizado com sucesso!' : 'Voto enviado com sucesso!'
    
    if (!existingVoteId.value && data.id) {
      existingVoteId.value = data.id
    }
  } catch (error) {
    console.error('Submit vote error:', error)
    errorMessage.value = error.message || 'Um erro aconteceu ao enviar seu voto. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (token && userId) {
    fetchPoll()
  } else {
    errorMessage.value = 'Usuário não autenticado'
  }
})
</script>

<template>
  <fieldset 
    class="fieldset bg-base-100 border-base-300 rounded-box border w-64 p-4 flex flex-col"
    :class="{ 'opacity-60': isLoading }"
  >
    <legend class="fieldset-legend text-lg font-semibold">{{ day }}</legend>

    <!-- Aviso de horário -->
    <div v-if="timeWarning" class="alert alert-info mb-3 py-2 text-sm">
      <span>{{ timeWarning }}</span>
    </div>

    <!-- Loading skeleton -->
    <div v-if="isLoading && !selectedOption" class="space-y-2">
      <div class="skeleton h-8 w-full"></div>
      <div class="skeleton h-8 w-full"></div>
      <div class="skeleton h-8 w-full"></div>
      <div class="skeleton h-8 w-full"></div>
    </div>

    <!-- Opções de voto -->
    <div v-else class="space-y-2">
      <LabelComponent 
        :for="`${name}-1`" 
        class="text-lg cursor-pointer hover:bg-base-200 p-2 rounded transition-colors"
        :class="{ 'opacity-50 cursor-not-allowed': isOptionDisabled('round_trip') }"
      >
        <div class="flex items-center gap-2">
          <input
            type="radio"
            class="radio radio-primary"
            :name="name"
            value="round_trip"
            v-model="selectedOption"
            :id="`${name}-1`"
            :disabled="isOptionDisabled('round_trip')"
          />
          <span>Ida e volta</span>
          <span 
            v-if="isOptionDisabled('round_trip')" 
            class="badge badge-sm badge-ghost"
            :title="getDisabledTooltip('round_trip')"
          >
            até 12h
          </span>
        </div>
      </LabelComponent>

      <LabelComponent 
        :for="`${name}-2`" 
        class="text-lg cursor-pointer hover:bg-base-200 p-2 rounded transition-colors"
        :class="{ 'opacity-50 cursor-not-allowed': isOptionDisabled('one_way_outbound') }"
      >
        <div class="flex items-center gap-2">
          <input
            type="radio"
            class="radio radio-primary"
            :name="name"
            value="one_way_outbound"
            v-model="selectedOption"
            :id="`${name}-2`"
            :disabled="isOptionDisabled('one_way_outbound')"
          />
          <span>Apenas ida</span>
          <span 
            v-if="isOptionDisabled('one_way_outbound')" 
            class="badge badge-sm badge-ghost"
            :title="getDisabledTooltip('one_way_outbound')"
          >
            até 12h
          </span>
        </div>
      </LabelComponent>

      <LabelComponent 
        :for="`${name}-3`" 
        class="text-lg cursor-pointer hover:bg-base-200 p-2 rounded transition-colors"
        :class="{ 'opacity-50 cursor-not-allowed': isOptionDisabled('one_way_return') }"
      >
        <div class="flex items-center gap-2">
          <input
            type="radio"
            class="radio radio-primary"
            :name="name"
            value="one_way_return"
            v-model="selectedOption"
            :id="`${name}-3`"
            :disabled="isOptionDisabled('one_way_return')"
          />
          <span>Apenas volta</span>
          <span 
            v-if="isOptionDisabled('one_way_return')" 
            class="badge badge-sm badge-ghost"
            :title="getDisabledTooltip('one_way_return')"
          >
            até 18h
          </span>
        </div>
      </LabelComponent>

      <LabelComponent 
        :for="`${name}-4`" 
        class="text-lg cursor-pointer hover:bg-base-200 p-2 rounded transition-colors"
        :class="{ 'opacity-50 cursor-not-allowed': isOptionDisabled('absent') }"
      >
        <div class="flex items-center gap-2">
          <input
            type="radio"
            class="radio radio-primary"
            :name="name"
            value="absent"
            v-model="selectedOption"
            :id="`${name}-4`"
            :disabled="isOptionDisabled('absent')"
          />
          <span>Não vou</span>
          <span 
            v-if="isOptionDisabled('absent')" 
            class="badge badge-sm badge-ghost"
            :title="getDisabledTooltip('absent')"
          >
            até 18h
          </span>
        </div>
      </LabelComponent>
    </div>

    <button 
      class="btn btn-primary mt-4" 
      @click="submitVote"
      :disabled="isLoading || !selectedOption || !canVoteInSelectedOption"
      :class="{ 'loading': isLoading }"
    >
      <span v-if="!isLoading">
        {{ existingVoteId ? 'Atualizar Voto' : 'Enviar Resposta' }}
      </span>
      <span v-else>Enviando...</span>
    </button>

    <!-- Mensagens de erro -->
    <div v-if="errorMessage" class="mt-3">
      <div class="alert alert-error py-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-sm">{{ errorMessage }}</span>
      </div>
    </div>

    <!-- Mensagens de sucesso -->
    <div v-if="successMessage" class="mt-3">
      <div class="alert alert-success py-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-sm">{{ successMessage }}</span>
      </div>
    </div>
  </fieldset>
</template>