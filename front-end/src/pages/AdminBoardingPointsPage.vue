<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import BoardingPointTableRow from '@/components/BoardingPointTableRow.vue'
import BoardingPointEditModal from '@/components/BoardingPointEditModal.vue'
import SortableTableHeader from '@/components/SortableTableHeader.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const boardingPoints = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const editingPoint = ref(null)
const showEditModal = ref(false)
const sortField = ref('route_order')
const sortDirection = ref('asc')

const sortedBoardingPoints = computed(() => {
  if (!sortField.value) {
    return boardingPoints.value
  }

  const sorted = [...boardingPoints.value].sort((a, b) => {
    let valueA = a[sortField.value]
    let valueB = b[sortField.value]

    if (typeof valueA === 'string') {
      valueA = valueA.toLowerCase()
      valueB = valueB.toLowerCase()
    }

    if (valueA < valueB) return sortDirection.value === 'asc' ? -1 : 1
    if (valueA > valueB) return sortDirection.value === 'asc' ? 1 : -1
    return 0
  })

  return sorted
})

function handleSort(field) {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
}

async function fetchBoardingPoints() {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}boarding-points/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao carregar pontos de embarque')
    }

    const data = await response.json()
    boardingPoints.value = data
  } catch (error) {
    console.error('Error fetching boarding points:', error)
    errorMessage.value = 'Erro ao carregar pontos de embarque. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

function openCreateModal() {
  editingPoint.value = null
  showEditModal.value = true
  errorMessage.value = ''
  successMessage.value = ''
}

function openEditModal(point) {
  editingPoint.value = point
  showEditModal.value = true
  errorMessage.value = ''
  successMessage.value = ''
}

function closeEditModal() {
  showEditModal.value = false
  editingPoint.value = null
}

async function savePoint(formData) {
  errorMessage.value = ''
  successMessage.value = ''

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    return
  }

  try {
    const isEdit = !!editingPoint.value
    const url = isEdit
      ? `${API_BASE_URL}boarding-points/${editingPoint.value.id}/`
      : `${API_BASE_URL}boarding-points/`

    const method = isEdit ? 'PATCH' : 'POST'

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
      body: JSON.stringify(formData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao salvar ponto de embarque')
    }

    successMessage.value = isEdit
      ? 'Ponto de embarque atualizado com sucesso!'
      : 'Ponto de embarque criado com sucesso!'

    await fetchBoardingPoints()

    setTimeout(() => {
      closeEditModal()
      successMessage.value = ''
    }, 1500)
  } catch (error) {
    console.error('Error saving boarding point:', error)
    errorMessage.value = error.message || 'Erro ao salvar. Tente novamente.'
  }
}

async function deletePoint(point) {
  if (!confirm(`Deseja realmente excluir o ponto "${point.name}"?`)) {
    return
  }

  errorMessage.value = ''
  successMessage.value = ''

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}boarding-points/${point.id}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao excluir ponto de embarque')
    }

    successMessage.value = 'Ponto de embarque excluído com sucesso!'
    await fetchBoardingPoints()

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error('Error deleting boarding point:', error)
    errorMessage.value = error.message || 'Erro ao excluir. Tente novamente.'
  }
}

onMounted(() => {
  fetchBoardingPoints()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-4xl font-bold mb-2">Gestão de Pontos de Embarque</h1>
            <p class="text-base-content/70">Gerencie os pontos de embarque e sua ordem na rota</p>
          </div>
          <button class="btn btn-primary" @click="openCreateModal">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Novo Ponto
          </button>
        </div>
      </div>

      <div v-if="successMessage" class="alert alert-success mb-4">
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
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ successMessage }}</span>
      </div>

      <div v-if="errorMessage" class="alert alert-error mb-4">
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
        <span>{{ errorMessage }}</span>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <div v-else class="card bg-base-100 shadow-xl">
        <div class="card-body p-0">
          <div class="overflow-x-auto">
            <table class="table table-zebra">
              <thead class="bg-base-200 sticky top-0 z-10">
                <tr>
                  <SortableTableHeader
                    label="Ordem"
                    field="route_order"
                    :current-sort="sortField"
                    :current-direction="sortDirection"
                    @sort="handleSort"
                  />
                  <SortableTableHeader
                    label="Nome"
                    field="name"
                    :current-sort="sortField"
                    :current-direction="sortDirection"
                    @sort="handleSort"
                  />
                  <th>Referência</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <BoardingPointTableRow
                  v-for="point in sortedBoardingPoints"
                  :key="point.id"
                  :point="point"
                  @edit="openEditModal"
                  @delete="deletePoint"
                />
              </tbody>
            </table>
          </div>

          <div v-if="!boardingPoints.length && !isLoading" class="text-center py-12">
            <div class="text-6xl mb-4 opacity-30">📍</div>
            <p class="text-base-content/60">Nenhum ponto de embarque cadastrado</p>
            <button class="btn btn-primary mt-4" @click="openCreateModal">
              Criar primeiro ponto
            </button>
          </div>
        </div>
      </div>

      <BoardingPointEditModal
        :show="showEditModal"
        :point="editingPoint"
        :existing-orders="boardingPoints.map((p) => p.route_order)"
        :success-message="successMessage"
        :error-message="errorMessage"
        @close="closeEditModal"
        @save="savePoint"
      />
    </div>
  </DefaultLayout>
</template>
