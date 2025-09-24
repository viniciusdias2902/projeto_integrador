<script setup>
const props = defineProps({ title: String })
</script>

<template>
  <fieldset
    class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4"
    @submit.prevent
  >
    <legend class="fieldset-legend">{{ title }}</legend>
    <slot></slot>
  </fieldset>
</template>
