<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'

const props = defineProps({
  boardingType: String,
  pollId: Number,
  pollDate: String,
})

const BOARDING_LIST_URL = `${import.meta.env.VITE_APP_API_URL}polls/`

const boardingPoints = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

// ✅ Função auxiliar para obter o token atualizado
function getToken() {
  return localStorage.getItem('access')
}

// Mapear tipo de viagem para o parâmetro da API
const tripTypeParam = computed(() => {
  return props.boardingType === 'Ida' ? 'outbound' : 'return'
})

// Computed para o título do grupo (ponto ou universidade)
const groupTitle = computed(() => {
  return props.boardingType === 'Ida' ? 'Ponto de Embarque' : 'Universidade'
})

// Computed para obter o nome do grupo
function getGroupName(item) {
  if (props.boardingType === 'Ida') {
    return item.point.name
  } else {
    // Mapeamento de nomes de universidades
    const universityNames = {
      IFPI: 'Instituto Federal do Piauí',
      CHRISFAPI: 'Christus Faculdade do Piauí',
      UESPI: 'Universidade Estadual do Piauí',
      ETC: 'Outra',
    }
    return universityNames[item.group_name] || item.group_name
  }
}

// Computed para obter referência adicional (apenas para ida)
function getGroupReference(item) {
  if (props.boardingType === 'Ida' && item.point?.address_reference) {
    return item.point.address_reference
  }
  return null
}

async function loadBoardingData() {
  if (!props.pollId) {
    errorMessage.value = 'ID da enquete não fornecido.'
    isLoading.value = false
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  // ✅ Verificar e renovar token antes da requisição
  const isValid = await verifyAndRefreshToken()

  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    isLoading.value = false
    return
  }

  try {
    const url = `${BOARDING_LIST_URL}${props.pollId}/boarding_list/?trip_type=${tripTypeParam.value}`

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${getToken()}`, // ✅ Obter token atualizado
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || error.detail || 'Erro ao carregar lista de embarque')
    }

    const data = await response.json()
    boardingPoints.value = data

    console.log(`Boarding list (${props.boardingType}):`, data)
  } catch (error) {
    console.error('Error loading boarding data:', error)
    errorMessage.value = error.message || 'Erro ao carregar lista. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadBoardingData()
})

// Expor função para permitir refresh externo
defineExpose({ refresh: loadBoardingData })
</script>

<template>
  <div class="card bg-base-100 shadow-xl border border-base-300">
    <div class="card-body">
      <!-- Cabeçalho -->
      <div class="flex items-center justify-between mb-4">
        <h2 class="card-title text-2xl">
          {{ boardingType }}
        </h2>
        <button
          class="btn btn-ghost btn-sm btn-circle"
          @click="loadBoardingData"
          :disabled="isLoading"
          title="Atualizar lista"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            :class="{ 'animate-spin': isLoading }"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
        </button>
      </div>

      <!-- Loading skeleton -->
      <div v-if="isLoading" class="space-y-4">
        <div class="skeleton h-20 w-full"></div>
        <div class="skeleton h-20 w-full"></div>
        <div class="skeleton h-20 w-full"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="errorMessage" class="alert alert-error">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span class="text-sm">{{ errorMessage }}</span>
      </div>

      <!-- Empty state -->
      <div v-else-if="boardingPoints.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4 opacity-30">📭</div>
        <p class="text-base-content/60">Nenhum aluno confirmado para esta viagem</p>
      </div>

      <!-- Boarding points list -->
      <div v-else class="space-y-4">
        <!-- Points ou Universities -->
        <div
          v-for="item in boardingPoints"
          :key="item.point?.id || item.group_name"
          class="bg-base-200 rounded-box p-4"
        >
          <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
            {{ item.point?.name || item.group_name }}
            <span v-if="item.point?.address_reference" class="text-sm font-normal opacity-60">
              ({{ item.point.address_reference }})
            </span>
          </h3>

          <ul class="menu bg-base-100 rounded-box">
            <li
              v-for="student in item.students"
              :key="student.id"
              class="border-b border-base-300 last:border-0"
            >
              <div class="py-3 hover:bg-base-200">
                <span class="font-medium">{{ student.name }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
