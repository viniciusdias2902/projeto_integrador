<script setup>
import { ref, onMounted } from 'vue';
import { getBoardingList } from '@/services/polls';
import ListRow from './ListRow.vue';

const props = defineProps({
  boardingType: String,
  pollId: Number,
});

const boardingPoints = ref([]);
const isLoading = ref(true);
const error = ref(null);

const loadBoardingData = async () => {
    error.value = 'ID da enquete não fornecido.';
    isLoading.value = false;
  

    const tripType = props.boardingType === 'Ida' ? 'one_way_outbound' : 'one_way_return';

    const data = await getBoardingList(props.pollId, tripType);
    boardingPoints.value = data;
 
};

onMounted(() => {
  loadBoardingData();
});
</script>

<template>
  <div class="shadow-md rounded-box p-6 w-full flex-col">
    <h2 class="text-xl font-bold mb-4">{{ boardingType }}</h2>

    <div v-if="isLoading">
      <p>Carregando...</p>
    </div>
    
    <div v-else-if="error">
      <p class="text-red-500">Erro: {{ error }}</p>
    </div>
    
    <div v-else-if="boardingPoints.length === 0">
      <p>Nenhum aluno confirmado para esta viagem.</p>
    </div>

    <div v-else>
      <div v-for="pointData in boardingPoints" :key="pointData.point.id" class="mb-6">
        <h3 class="font-semibold text-lg border-b pb-2 mb-2">
          📍 {{ pointData.point.name }} ({{ pointData.students.length }} alunos)
        </h3>
        <ul class="list bg-base-100 rounded-box shadow-sm max-h-80 overflow-y-auto">
          <ListRow
            v-for="(student, index) in pointData.students"
            :key="student.id"
            :index="index + 1"
            :title="student.name"
            description="" 
          />
        </ul>
      </div>
    </div>
  </div>
</template>