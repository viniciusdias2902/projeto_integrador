<script setup>
defineProps({ for: String })
</script>

<template>
  <label class="label" :for="for"><slot></slot></label>
</template>
