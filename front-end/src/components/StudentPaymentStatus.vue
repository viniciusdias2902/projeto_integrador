<script setup>
import { computed } from 'vue'
import { parseLocalDate } from '@/utils/dateUtils'

const props = defineProps({
  lastPaymentDate: {
    type: String,
    default: null,
  },
})

const paymentStatus = computed(() => {
  if (!props.lastPaymentDate || props.lastPaymentDate === 'não informado') {
    return {
      label: 'Não informado',
      color: 'badge-ghost',
    }
  }

  const lastPayment = parseLocalDate(props.lastPaymentDate)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const daysSincePayment = Math.floor((today - lastPayment) / (1000 * 60 * 60 * 24))

  if (daysSincePayment > 35) {
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
})
</script>

<template>
  <span class="badge" :class="paymentStatus.color">
    {{ paymentStatus.label }}
  </span>
</template>
