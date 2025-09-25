<script setup>
import { ref, onMounted } from 'vue';
import { getBoardingList } from '@/services/polls';
import ListRow from './ListRow.vue';

const props = defineProps({
  boardingType: String,
});

const boardingPoints = ref([]); 
const isLoading = ref(true);    
const error = ref(null); 

const loadBoardingData = async () => {
  try {
    const pollId = 1;
    
    const tripType = props.boardingType === 'Ida' ? 'one_way_outbound' : 'one_way_return';

    const data = await getBoardingList(pollId, tripType);
    boardingPoints.value = data; 
  } catch (err) {
    error.value = err.message; 
  } finally {
    isLoading.value = false; 
  }
};


onMounted(() => {
  loadBoardingData();
});
</script>

<template>
  <div class="shadow-md rounded-box p-6 w-full flex-col">
    <h2 class="text-xl font-bold mb-4">{{ boardingType }}</h2>

    
    <div v-else-if="error">
      <p class="text-red-500">Erro: {{ error }}</p>
    </div>
    
    <div v-else-if="boardingPoints.length === 0">
      <p>Nenhum aluno confirmado para esta viagem.</p>
    </div>
  </div>
</template>