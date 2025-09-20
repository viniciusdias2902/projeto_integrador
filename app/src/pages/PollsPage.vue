<script setup lang="ts">
import DefaultLayout from '@/templates/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 my-8">
      <PollComponent v-for="n in 6"></PollComponent>
    </div>
  </DefaultLayout>
</template>
