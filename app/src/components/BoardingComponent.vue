<script setup>
const props = defineProps({
  boardingType: String,
})
</script>

<template>
  <div class="shadow-md rounded-box p-6 w-80 flex-col items-center justify-center">
    <h2 class="text-xl font-bold mb-4">{{ boardingType }}</h2>
    <div>
      <ul class="list bg-base-100 rounded-box shadow-md">
        <li class="list-row">
          <div class="text-4xl font-thin opacity-30 tabular-nums">01</div>
          <div class="list-col-grow">
            <div>Literalmente a Sabrina Carpenter</div>
            <div class="text-xs uppercase font-semibold opacity-60">Vale Lehigh</div>
          </div>
        </li>

        <li class="list-row">
          <div class="text-4xl font-thin opacity-30 tabular-nums">02</div>
          <div class="list-col-grow">
            <div>Katie Bouman</div>
            <div class="text-xs uppercase font-semibold opacity-60">MIT</div>
          </div>
        </li>

        <li class="list-row">
          <div class="text-4xl font-thin opacity-30 tabular-nums">03</div>
          <div class="list-col-grow">
            <div>Danilo</div>
            <div class="text-xs uppercase font-semibold opacity-60">Gado Bravo</div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
