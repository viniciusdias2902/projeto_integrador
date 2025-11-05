<script setup>
import { ref, watch, computed } from 'vue'

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

const monthlyPaymentReais = ref('')
const lastPaymentDate = ref(null)

watch(
  () => props.student,
  (newStudent) => {
    if (newStudent) {
      if (
        newStudent.monthly_payment_cents &&
        newStudent.monthly_payment_cents !== 'não informado'
      ) {
        monthlyPaymentReais.value = (newStudent.monthly_payment_cents / 100).toFixed(2)
      } else {
        monthlyPaymentReais.value = ''
      }

      lastPaymentDate.value =
        newStudent.last_payment_date === 'não informado' ? null : newStudent.last_payment_date
    }
  },
)

const currentPaymentDisplay = computed(() => {
  if (!props.student) return 'Não informado'
  const cents = props.student.monthly_payment_cents
  if (cents === null || cents === undefined || cents === 'não informado') {
    return 'Não informado'
  }
  return `R$ ${(cents / 100).toFixed(2).replace('.', ',')}`
})

const currentDateDisplay = computed(() => {
  if (!props.student) return 'Não informado'
  const dateString = props.student.last_payment_date
  if (!dateString || dateString === 'não informado') {
    return 'Não informado'
  }
  return new Date(dateString).toLocaleDateString('pt-BR')
})

function handleSave() {
  const data = {
    last_payment_date: lastPaymentDate.value,
  }

  if (monthlyPaymentReais.value && monthlyPaymentReais.value.trim() !== '') {
    const valueStr = monthlyPaymentReais.value.replace(',', '.')
    const valueFloat = parseFloat(valueStr)

    if (!isNaN(valueFloat)) {
      data.monthly_payment_cents = Math.round(valueFloat * 100)
    }
  } else {
    data.monthly_payment_cents = null
  }

  emit('save', data)
}

function handleClose() {
  emit('close')
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
          <span class="label-text">Mensalidade</span>
        </label>
        <label class="input input-bordered flex items-center gap-2">
          <span class="text-base-content/70">R$</span>
          <input
            v-model="monthlyPaymentReais"
            type="text"
            placeholder="500.00"
            class="grow"
            @input="monthlyPaymentReais = monthlyPaymentReais.replace(/[^\d.,]/g, '')"
          />
        </label>
        <label class="label">
          <span class="label-text-alt"> Valor atual: {{ currentPaymentDisplay }} </span>
        </label>
      </div>

      <div class="form-control w-full mb-4">
        <label class="label">
          <span class="label-text">Data do Último Pagamento</span>
        </label>
        <input v-model="lastPaymentDate" type="date" class="input input-bordered w-full" />
        <label class="label">
          <span class="label-text-alt"> Data atual: {{ currentDateDisplay }} </span>
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
