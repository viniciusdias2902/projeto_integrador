<script setup>
import ListRow from './ListRow.vue'

defineProps({
  boardingType: String,
})
</script>

<template>
  <div class="shadow-md rounded-box p-6 w-80 flex-col items-center justify-center">
    <h2 class="text-xl font-bold mb-4">{{ boardingType }}</h2>
    <div>
      <ul class="list bg-base-100 rounded-box shadow-md max-h-100 overflow-scroll">
        <ListRow
          v-for="n in 20"
          :key="n"
          :index="n"
          title="Danilo"
          description="Gado bravo"
        ></ListRow>
      </ul>
    </div>
  </div>
</template>
