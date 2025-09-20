<script setup>
import DefaultLayout from './templates/DefaultLayout.vue'
</script>

<template>
  <div class="flex h-screen flex-col items-center">
    <DefaultLayout />
    <main class="flex-1 flex items-center justify-center">
      <LoginComponent />
    </main>
  </div>
</template>

<style scoped></style>
