<script setup>
const props = defineProps({
  boardingType: String,
})
</script>

<template>
  <div class="shadow-md rounded-box p-6 w-80 flex-col items-center justify-center">
    <h2 class="text-xl font-bold mb-4">{{ boardingType }}</h2>
    <ol class="list-decimal list-inside space-y-1">
      <li>Fulano</li>
      <li>Ciclano</li>
      <li>Beltrano</li>
      <li>Fulano</li>
      <li>Ciclano</li>
      <li>Beltrano</li>
      <li>Fulano</li>
      <li>Ciclano</li>
      <li>Beltrano</li>
      <li>Fulano</li>
      <li>Ciclano</li>
      <li>Beltrano</li>
      <li>Fulano</li>
      <li>Ciclano</li>
      <li>Beltrano</li>
    </ol>
  </div>
</template>
