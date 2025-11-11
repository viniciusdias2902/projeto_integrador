<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  point: {
    type: Object,
    default: null,
  },
  existingOrders: {
    type: Array,
    default: () => [],
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

const name = ref('')
const addressReference = ref('')
const routeOrder = ref(0)

const isEdit = computed(() => !!props.point)

const modalTitle = computed(() => {
  return isEdit.value ? 'Editar Ponto de Embarque' : 'Novo Ponto de Embarque'
})

const nextAvailableOrder = computed(() => {
  if (props.existingOrders.length === 0) return 0
  return Math.max(...props.existingOrders) + 1
})

watch(
  () => props.point,
  (newPoint) => {
    if (newPoint) {
      name.value = newPoint.name || ''
      addressReference.value = newPoint.address_reference || ''
      routeOrder.value = newPoint.route_order
    } else {
      name.value = ''
      addressReference.value = ''
      routeOrder.value = nextAvailableOrder.value
    }
  },
  { immediate: true },
)

watch(
  () => props.show,
  (newShow) => {
    if (newShow && !props.point) {
      routeOrder.value = nextAvailableOrder.value
    }
  },
)

function handleSave() {
  if (!name.value.trim()) {
    return
  }

  const data = {
    name: name.value.trim(),
    address_reference: addressReference.value.trim() || null,
    route_order: routeOrder.value,
  }

  emit('save', data)
}

function handleClose() {
  emit('close')
}
</script>

<template>
  <dialog :class="{ 'modal-open': show }" class="modal">
    <div class="modal-box max-w-2xl">
      <h3 class="font-bold text-lg mb-4">{{ modalTitle }}</h3>

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
          <span class="label-text">Nome do Ponto</span>
        </label>
        <input
          v-model="name"
          type="text"
          placeholder="Ex: Praça Central"
          class="input input-bordered w-full"
          required
        />
      </div>

      <div class="form-control w-full mb-4">
        <label class="label">
          <span class="label-text">Referência</span>
        </label>
        <input
          v-model="addressReference"
          type="text"
          placeholder="Ex: Em frente à farmácia"
          class="input input-bordered w-full"
        />
        <label class="label">
          <span class="label-text-alt">Opcional</span>
        </label>
      </div>

      <div class="form-control w-full mb-4">
        <label class="label">
          <span class="label-text">Posição na Rota</span>
        </label>
        <input
          v-model.number="routeOrder"
          type="number"
          min="0"
          class="input input-bordered w-full"
          required
        />
        <label class="label">
          <span class="label-text-alt">
            Os pontos seguintes serão reordenados automaticamente
          </span>
        </label>
      </div>

      <div class="modal-action">
        <button class="btn" @click="handleClose">Cancelar</button>
        <button class="btn btn-primary" @click="handleSave" :disabled="!name.trim()">Salvar</button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop" @click="handleClose">
      <button>close</button>
    </form>
  </dialog>
</template>
