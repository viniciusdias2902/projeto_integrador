<script setup lang="ts">
import DefaultLayout from '@/templates/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <BoardingComponent boardingType="Ida" />
      <BoardingComponent boardingType="Volta" />
    </div>
  </DefaultLayout>
</template>
