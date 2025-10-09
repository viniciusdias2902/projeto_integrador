<template>
  <p v-if="message" class="text-red-600 text-sm mt-1">{{ message }}</p>
</template>

<script>
export default {
  name: 'ValidationMessage',
  props: {
    message: String,
  },
}
</script>
