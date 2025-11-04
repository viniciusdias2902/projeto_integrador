<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  student: {
    type: Object,
    default: null,
  },
  successMessage: {
    type: String,
    default: '',
  },
  errorMessage: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close', 'save'])

const form = ref({
  monthly_payment_cents: null,
  last_payment_date: null,
})

watch(
  () => props.student,
  (newStudent) => {
    if (newStudent) {
      form.value = {
        monthly_payment_cents:
          newStudent.monthly_payment_cents === 'não informado'
            ? null
            : newStudent.monthly_payment_cents,
        last_payment_date:
          newStudent.last_payment_date === 'não informado' ? null : newStudent.last_payment_date,
      }
    }
  },
)

function handleSave() {
  emit('save', form.value)
}

function handleClose() {
  emit('close')
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
  return new Date(dateString).toLocaleDateString('pt-BR')
}
</script>

<template>
  <dialog :class="{ 'modal-open': show }" class="modal">
    <div class="modal-box">
      <h3 class="font-bold text-lg mb-4">Editar Pagamento - {{ student?.name }}</h3>

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
          v-model.number="form.monthly_payment_cents"
          type="number"
          placeholder="Ex: 50000 (R$ 500,00)"
          class="input input-bordered w-full"
          min="0"
        />
        <label class="label">
          <span class="label-text-alt">
            Valor atual: {{ formatCurrency(student?.monthly_payment_cents) }}
          </span>
        </label>
      </div>

      <div class="form-control w-full mb-4">
        <label class="label">
          <span class="label-text">Data do Último Pagamento</span>
        </label>
        <input v-model="form.last_payment_date" type="date" class="input input-bordered w-full" />
        <label class="label">
          <span class="label-text-alt">
            Data atual: {{ formatDate(student?.last_payment_date) }}
          </span>
        </label>
      </div>

      <div class="modal-action">
        <button class="btn" @click="handleClose">Cancelar</button>
        <button class="btn btn-primary" @click="handleSave">Salvar</button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop" @click="handleClose">
      <button>close</button>
    </form>
  </dialog>
</template>
