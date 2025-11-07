<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  students: {
    type: Array,
    required: true,
  },
})

const chartCanvas = ref(null)
let chartInstance = null

function parseLocalDate(dateString) {
  if (!dateString || dateString === 'não informado') {
    return null
  }
  const [year, month, day] = dateString.split('-').map(Number)
  return new Date(year, month - 1, day)
}

function getPaymentStatus(student) {
  if (!student.last_payment_date || student.last_payment_date === 'não informado') {
    return 'not_paid'
  }

  const lastPayment = parseLocalDate(student.last_payment_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const daysSincePayment = Math.floor((today - lastPayment) / (1000 * 60 * 60 * 24))

  if (daysSincePayment > 35) {
    return 'overdue'
  } else if (daysSincePayment >= 30) {
    return 'should_pay'
  } else {
    return 'up_to_date'
  }
}

const paymentStats = computed(() => {
  const stats = {
    up_to_date: 0,
    should_pay: 0,
    overdue: 0,
    not_paid: 0,
  }

  props.students.forEach((student) => {
    const status = getPaymentStatus(student)
    stats[status]++
  })

  return stats
})

function createChart() {
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Em dia', 'Deve pagar', 'Atrasado', 'Não informado'],
      datasets: [
        {
          data: [
            paymentStats.value.up_to_date,
            paymentStats.value.should_pay,
            paymentStats.value.overdue,
            paymentStats.value.not_paid,
          ],
          backgroundColor: [
            'oklch(62% 0.194 149.214)',
            'oklch(85% 0.199 91.936)',
            'oklch(70% 0.191 22.216)',
            'oklch(86% 0 0)',
          ],
          borderWidth: 2,
          borderColor: 'oklch(100% 0 0)',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            font: {
              size: 14,
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || ''
              const value = context.parsed || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
              return `${label}: ${value} (${percentage}%)`
            },
          },
        },
      },
    },
  })
}

watch(
  () => props.students,
  () => {
    nextTick(() => {
      createChart()
    })
  },
  { deep: true },
)

onMounted(() => {
  createChart()
})
</script>

<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">Status de Pagamento</h2>
      <div class="w-full h-96">
        <canvas ref="chartCanvas"></canvas>
      </div>
      <div class="stats stats-vertical lg:stats-horizontal shadow mt-4">
        <div class="stat">
          <div class="stat-title">Em dia</div>
          <div class="stat-value text-success">{{ paymentStats.up_to_date }}</div>
        </div>
        <div class="stat">
          <div class="stat-title">Deve pagar</div>
          <div class="stat-value text-warning">{{ paymentStats.should_pay }}</div>
        </div>
        <div class="stat">
          <div class="stat-title">Atrasado</div>
          <div class="stat-value text-error">{{ paymentStats.overdue }}</div>
        </div>
        <div class="stat">
          <div class="stat-title">Não informado</div>
          <div class="stat-value">{{ paymentStats.not_paid }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
