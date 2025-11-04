<script setup>
import StudentPaymentStatus from './StudentPaymentStatus.vue'

defineProps({
  student: {
    type: Object,
    required: true,
  },
  universities: {
    type: Object,
    required: true,
  },
  shifts: {
    type: Object,
    required: true,
  },
})

defineEmits(['edit'])

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
  <tr class="hover">
    <td class="font-medium">{{ student.name }}</td>
    <td>{{ student.phone }}</td>
    <td>{{ universities[student.university] || student.university }}</td>
    <td>
      <span class="badge badge-ghost">
        {{ shifts[student.class_shift] }}
      </span>
    </td>
    <td>{{ formatCurrency(student.monthly_payment_cents) }}</td>
    <td>{{ formatDate(student.last_payment_date) }}</td>
    <td>
      <StudentPaymentStatus :last-payment-date="student.last_payment_date" />
    </td>
    <td>
      <button class="btn btn-ghost btn-sm" @click="$emit('edit', student)">
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
</template>
