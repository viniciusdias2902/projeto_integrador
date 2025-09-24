<script setup>
defineProps({ index: Number, title: String, description: String })
</script>

<template>
  <li class="list-row">
    <div class="text-4xl font-thin opacity-30 tabular-nums">{{ index }}</div>
    <div class="list-col-grow">
      <div>{{ title }}</div>
      <div class="text-xs uppercase font-semibold opacity-60">{{ description }}</div>
    </div>
  </li>
</template>
