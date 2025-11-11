<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import StudentTableRow from '@/components/StudentTableRow.vue'
import StudentEditModal from '@/components/StudentEditModal.vue'
import SortableTableHeader from '@/components/SortableTableHeader.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const students = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const editingStudent = ref(null)
const showEditModal = ref(false)
const sortField = ref(null)
const sortDirection = ref('asc')

const universities = {
  UESPI: 'Universidade Estadual do Piauí',
  CHRISFAPI: 'Christus Faculdade do Piauí',
  IFPI: 'Instituto Federal do Piauí',
  ETC: 'Outro',
}

const shifts = {
  M: 'Manhã',
  A: 'Tarde',
  E: 'Noite',
  'M-A': 'Manhã/Tarde',
  'A-E': 'Tarde/Noite',
}

function parseLocalDate(dateString) {
  if (!dateString || dateString === 'não informado') {
    return null
  }
  const [year, month, day] = dateString.split('-').map(Number)
  return new Date(year, month - 1, day)
}

function getPaymentStatusValue(student) {
  if (!student.last_payment_date || student.last_payment_date === 'não informado') {
    return 3
  }

  const lastPayment = parseLocalDate(student.last_payment_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const daysSincePayment = Math.floor((today - lastPayment) / (1000 * 60 * 60 * 24))

  if (daysSincePayment > 35) {
    return 2
  } else if (daysSincePayment >= 30) {
    return 1
  } else {
    return 0
  }
}

const sortedStudents = computed(() => {
  if (!sortField.value) {
    return students.value
  }

  const sorted = [...students.value].sort((a, b) => {
    let valueA, valueB

    if (sortField.value === 'payment_status') {
      valueA = getPaymentStatusValue(a)
      valueB = getPaymentStatusValue(b)
    } else if (sortField.value === 'monthly_payment_cents') {
      valueA = a.monthly_payment_cents === 'não informado' ? 0 : a.monthly_payment_cents
      valueB = b.monthly_payment_cents === 'não informado' ? 0 : b.monthly_payment_cents
    } else {
      valueA = a[sortField.value]
      valueB = b[sortField.value]
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

async function fetchStudents() {
  errorMessage.value = ''
  isLoading.value = true

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}students/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao carregar estudantes')
    }

    const data = await response.json()
    students.value = data
  } catch (error) {
    console.error('Error fetching students:', error)
    errorMessage.value = 'Erro ao carregar estudantes. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

function openEditModal(student) {
  editingStudent.value = student
  showEditModal.value = true
  errorMessage.value = ''
  successMessage.value = ''
}

function closeEditModal() {
  showEditModal.value = false
  editingStudent.value = null
}

async function savePaymentInfo(formData) {
  if (!editingStudent.value) return

  errorMessage.value = ''
  successMessage.value = ''

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}students/${editingStudent.value.id}/payment/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
      body: JSON.stringify(formData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao atualizar informações de pagamento')
    }

    successMessage.value = 'Informações de pagamento atualizadas com sucesso!'
    await fetchStudents()

    setTimeout(() => {
      closeEditModal()
    }, 1500)
  } catch (error) {
    console.error('Error updating payment info:', error)
    errorMessage.value = error.message || 'Erro ao atualizar. Tente novamente.'
  }
}

function escapeCSV(value) {
  if (value === null || value === undefined) {
    return ''
  }

  const stringValue = String(value)

  if (stringValue.includes('"') || stringValue.includes(',') || stringValue.includes('\n')) {
    return `"${stringValue.replace(/"/g, '""')}"`
  }

  return stringValue
}

function formatCurrency(cents) {
  if (cents === null || cents === undefined || cents === 'não informado') {
    return 'Não informado'
  }
  return `R$ ${(cents / 100).toFixed(2).replace('.', ',')}`
}

function formatDate(dateString) {
  if (!dateString || dateString === 'não informado') {
    return 'Não informado'
  }
  const date = parseLocalDate(dateString)
  if (!date) return 'Não informado'
  return date.toLocaleDateString('pt-BR')
}

function getPaymentStatus(student) {
  if (!student.last_payment_date || student.last_payment_date === 'não informado') {
    return 'Não informado'
  }

  const lastPayment = parseLocalDate(student.last_payment_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const daysSincePayment = Math.floor((today - lastPayment) / (1000 * 60 * 60 * 24))

  if (daysSincePayment > 35) {
    return 'Atrasado'
  } else if (daysSincePayment >= 30) {
    return 'Deve pagar'
  } else {
    return 'Em dia'
  }
}

function exportToCSV() {
  const headers = [
    'Nome',
    'Telefone',
    'Universidade',
    'Turno',
    'Mensalidade',
    'Última Data de Pagamento',
    'Status de Pagamento',
  ]

  const rows = students.value.map((student) => {
    return [
      escapeCSV(student.name),
      escapeCSV(student.phone),
      escapeCSV(universities[student.university] || student.university),
      escapeCSV(shifts[student.class_shift] || student.class_shift),
      escapeCSV(formatCurrency(student.monthly_payment_cents)),
      escapeCSV(formatDate(student.last_payment_date)),
      escapeCSV(getPaymentStatus(student)),
    ]
  })

  const csvLines = [headers.join(',')]
  rows.forEach((row) => {
    csvLines.push(row.join(','))
  })

  const csvContent = csvLines.join('\n')
  const BOM = '\uFEFF'
  const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })

  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `estudantes_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  URL.revokeObjectURL(url)
}

onMounted(() => {
  fetchStudents()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-4xl font-bold mb-2">Gestão de Estudantes</h1>
            <p class="text-base-content/70">Gerencie pagamentos e informações dos estudantes</p>
          </div>
          <button
            class="btn btn-primary"
            @click="exportToCSV"
            :disabled="isLoading || students.length === 0"
          >
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
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Exportar como CSV
          </button>
        </div>
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
                  <th>Nome</th>
                  <th>Telefone</th>
                  <th>Universidade</th>
                  <th>Turno</th>
                  <SortableTableHeader
                    label="Mensalidade"
                    field="monthly_payment_cents"
                    :current-sort="sortField"
                    :current-direction="sortDirection"
                    @sort="handleSort"
                  />
                  <th>Último Pagamento</th>
                  <SortableTableHeader
                    label="Status"
                    field="payment_status"
                    :current-sort="sortField"
                    :current-direction="sortDirection"
                    @sort="handleSort"
                  />
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <StudentTableRow
                  v-for="student in sortedStudents"
                  :key="student.id"
                  :student="student"
                  :universities="universities"
                  :shifts="shifts"
                  @edit="openEditModal"
                />
              </tbody>
            </table>
          </div>

          <div v-if="!students.length && !isLoading" class="text-center py-12">
            <div class="text-6xl mb-4 opacity-30">📚</div>
            <p class="text-base-content/60">Nenhum estudante cadastrado</p>
          </div>
        </div>
      </div>

      <StudentEditModal
        :show="showEditModal"
        :student="editingStudent"
        :success-message="successMessage"
        :error-message="errorMessage"
        @close="closeEditModal"
        @save="savePaymentInfo"
      />
    </div>
  </DefaultLayout>
</template>
