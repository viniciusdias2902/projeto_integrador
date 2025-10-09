<template>
  <div class="flex h-screen flex-col w-full">
    <NavBar />
    <main class="flex-1 flex items-center justify-center w-full px-4">
      <slot></slot>
    </main>
    <FooterComponent />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import FooterComponent from '@/components/FooterComponent.vue'
</script>
