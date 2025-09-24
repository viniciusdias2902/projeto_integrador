<script setup>
import LabelComponent from './LabelComponent.vue'

defineProps({ day: String, name: String })
</script>

<template>
  <fieldset class="fieldset bg-base-100 border-base-300 rounded-box border lg:w-200 sm:w-64 p-4">
    <legend class="fieldset-legend">{{ day }}</legend>
    <LabelComponent :for="`${name} - 1`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="round_trip"
        :id="`${name} - 1`"
      />
      Ida e volta
    </LabelComponent>
    <LabelComponent :for="`${name} - 2`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="one_way_outbound"
        :id="`${name} - 2`"
      />
      Apenas ida
    </LabelComponent>
    <LabelComponent :for="`${name} - 3`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="one_way_return"
        :id="`${name} - 3`"
      />
      Apenas volta
    </LabelComponent>
    <LabelComponent :for="`${name} - 4`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="absent"
        :id="`${name} - 4`"
      />
      Não vou
    </LabelComponent>
    <button class="btn btn-primary mt-1">Enviar esposta</button>
  </fieldset>
</template>
