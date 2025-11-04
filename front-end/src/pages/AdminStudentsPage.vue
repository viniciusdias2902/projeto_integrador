<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const students = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const editingStudent = ref(null)
const showEditModal = ref(false)

const editForm = ref({
  monthly_payment_cents: null,
  payment_day: null,
})

const universities = {
  UESPI: 'Universidade Estadual do Piauí',
  CHRISFAPI: 'Christus Faculdade do Piauí',
  IFPI: 'Instituto Federal do Piauí',
  ETC: 'Outro',
}

function formatCurrency(cents) {
  if (cents === null || cents === undefined || cents === 'não informado') {
    return 'Não informado'
  }
  return `R$ ${(cents / 100).toFixed(2).replace('.', ',')}`
}

function getPaymentStatus(student) {
  if (!student.payment_day || student.payment_day === 'não informado') {
    return {
      label: 'Não é possível calcular',
      color: 'badge-ghost',
    }
  }

  const today = new Date()
  const currentDay = today.getDate()
  const paymentDay = parseInt(student.payment_day)

  let daysSincePayment
  if (currentDay >= paymentDay) {
    daysSincePayment = currentDay - paymentDay
  } else {
    const lastMonth = new Date(today.getFullYear(), today.getMonth(), 0)
    const daysInLastMonth = lastMonth.getDate()
    daysSincePayment = daysInLastMonth - paymentDay + currentDay
  }

  if (daysSincePayment >= 35) {
    return {
      label: 'Atrasado',
      color: 'badge-error',
    }
  } else if (daysSincePayment >= 30) {
    return {
      label: 'Deve pagar',
      color: 'badge-warning',
    }
  } else {
    return {
      label: 'Em dia',
      color: 'badge-success',
    }
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
  editForm.value = {
    monthly_payment_cents:
      student.monthly_payment_cents === 'não informado' ? null : student.monthly_payment_cents,
    payment_day: student.payment_day === 'não informado' ? null : student.payment_day,
  }
  showEditModal.value = true
  errorMessage.value = ''
  successMessage.value = ''
}

function closeEditModal() {
  showEditModal.value = false
  editingStudent.value = null
  editForm.value = {
    monthly_payment_cents: null,
    payment_day: null,
  }
}

async function savePaymentInfo() {
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
      body: JSON.stringify(editForm.value),
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

function exportToDocument() {
  const headers = [
    'Nome',
    'Email',
    'Telefone',
    'Universidade',
    'Turno',
    'Mensalidade',
    'Dia de Pagamento',
    'Status',
  ]

  const shifts = {
    M: 'Manhã',
    A: 'Tarde',
    E: 'Noite',
    'M-A': 'Manhã e Tarde',
    'A-E': 'Tarde e Noite',
  }

  const rows = students.value.map((student) => {
    const status = getPaymentStatus(student)
    return [
      student.name,
      student.user?.email || 'N/A',
      student.phone,
      universities[student.university] || student.university,
      shifts[student.class_shift] || student.class_shift,
      formatCurrency(student.monthly_payment_cents),
      student.payment_day === 'não informado' ? 'Não informado' : student.payment_day,
      status.label,
    ]
  })

  let csvContent = 'data:text/csv;charset=utf-8,'
  csvContent += headers.join(',') + '\n'
  rows.forEach((row) => {
    csvContent += row.map((cell) => `"${cell}"`).join(',') + '\n'
  })

  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `estudantes_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  fetchStudents()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8">
      <!-- Cabeçalho -->
      <div class="mb-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-4xl font-bold mb-2">Gestão de Estudantes</h1>
            <p class="text-base-content/70">Gerencie pagamentos e informações dos estudantes</p>
          </div>
          <button class="btn btn-primary" @click="exportToDocument" :disabled="isLoading">
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

      <!-- Mensagens -->
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

      <!-- Loading -->
      <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- Tabela -->
      <div v-else class="card bg-base-100 shadow-xl">
        <div class="card-body p-0">
          <div class="overflow-x-auto">
            <table class="table table-zebra">
              <thead class="bg-base-200 sticky top-0 z-10">
                <tr>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Universidade</th>
                  <th>Turno</th>
                  <th>Mensalidade</th>
                  <th>Dia de Pagamento</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in students" :key="student.id" class="hover">
                  <td class="font-medium">{{ student.name }}</td>
                  <td>{{ student.user?.email || 'N/A' }}</td>
                  <td>{{ student.phone }}</td>
                  <td>{{ universities[student.university] || student.university }}</td>
                  <td>
                    <span class="badge badge-ghost">
                      {{
                        {
                          M: 'Manhã',
                          A: 'Tarde',
                          E: 'Noite',
                          'M-A': 'Manhã/Tarde',
                          'A-E': 'Tarde/Noite',
                        }[student.class_shift]
                      }}
                    </span>
                  </td>
                  <td>{{ formatCurrency(student.monthly_payment_cents) }}</td>
                  <td>
                    {{
                      student.payment_day === 'não informado'
                        ? 'Não informado'
                        : `Dia ${student.payment_day}`
                    }}
                  </td>
                  <td>
                    <span class="badge" :class="getPaymentStatus(student).color">
                      {{ getPaymentStatus(student).label }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-ghost btn-sm" @click="openEditModal(student)">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                      </svg>
                      Editar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Empty State -->
          <div v-if="!students.length && !isLoading" class="text-center py-12">
            <div class="text-6xl mb-4 opacity-30">📚</div>
            <p class="text-base-content/60">Nenhum estudante cadastrado</p>
          </div>
        </div>
      </div>

      <!-- Modal de Edição -->
      <dialog :class="{ 'modal-open': showEditModal }" class="modal">
        <div class="modal-box">
          <h3 class="font-bold text-lg mb-4">Editar Pagamento - {{ editingStudent?.name }}</h3>

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

          <div class="form-control w-full mb-4">
            <label class="label">
              <span class="label-text">Mensalidade (em centavos)</span>
            </label>
            <input
              v-model.number="editForm.monthly_payment_cents"
              type="number"
              placeholder="Ex: 50000 (R$ 500,00)"
              class="input input-bordered w-full"
              min="0"
            />
            <label class="label">
              <span class="label-text-alt">
                Valor atual:
                {{ formatCurrency(editingStudent?.monthly_payment_cents) }}
              </span>
            </label>
          </div>

          <div class="form-control w-full mb-4">
            <label class="label">
              <span class="label-text">Dia de Pagamento</span>
            </label>
            <input
              v-model.number="editForm.payment_day"
              type="number"
              placeholder="1-31"
              class="input input-bordered w-full"
              min="1"
              max="31"
            />
            <label class="label">
              <span class="label-text-alt">
                Dia atual:
                {{
                  editingStudent?.payment_day === 'não informado'
                    ? 'Não informado'
                    : `Dia ${editingStudent?.payment_day}`
                }}
              </span>
            </label>
          </div>

          <div class="modal-action">
            <button class="btn" @click="closeEditModal">Cancelar</button>
            <button class="btn btn-primary" @click="savePaymentInfo">Salvar</button>
          </div>
        </div>
        <form method="dialog" class="modal-backdrop" @click="closeEditModal">
          <button>close</button>
        </form>
      </dialog>
    </div>
  </DefaultLayout>
</template>
