<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DefaultLayout from '@/templates/DefaultLayout.vue';
import BoardingComponent from '@/components/BoardingComponent.vue';
import { getTodaysPoll } from '@/services/polls';

const todaysPoll = ref(null);
const isLoading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const poll = await getTodaysPoll();
    if (poll) {
      todaysPoll.value = poll;
    } else {
      error.value = "Nenhuma enquete encontrada para a data de hoje.";
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <DefaultLayout>
    <div v-if="isLoading" class="text-center p-10">
      <p>Buscando enquete do dia...</p>
    </div>

    <div v-else-if="error" class="text-center p-10 text-red-500">
      <p><b>Ocorreu um erro:</b> {{ error }}</p>
    </div>

    <div v-else-if="todaysPoll" class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <BoardingComponent boardingType="Ida" :pollId="todaysPoll.id" />
      <BoardingComponent boardingType="Volta" :pollId="todaysPoll.id" />
    </div>
  </DefaultLayout>
</template>