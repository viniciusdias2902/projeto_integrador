<script setup>
defineProps({
  point: {
    type: Object,
    required: true,
  },
})

defineEmits(['edit', 'delete'])
</script>

<template>
  <tr class="hover">
    <td>
      <div class="flex items-center gap-2">
        <span class="badge badge-primary">{{ point.route_order }}</span>
      </div>
    </td>
    <td class="font-medium">{{ point.name }}</td>
    <td>
      <span v-if="point.address_reference" class="text-sm">
        {{ point.address_reference }}
      </span>
      <span v-else class="text-sm opacity-50">Sem referência</span>
    </td>
    <td>
      <div class="flex gap-2">
        <button class="btn btn-ghost btn-sm" @click="$emit('edit', point)">
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
        <button class="btn btn-ghost btn-sm text-error" @click="$emit('delete', point)">
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
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
          Excluir
        </button>
      </div>
    </td>
  </tr>
</template>
