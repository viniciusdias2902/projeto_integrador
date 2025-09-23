<template>
  <div class="form-control">
    <label :for="id" class="label">
      <span class="label-text">{{ label }}</span>
    </label>
    <select
      :id="id"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      required
      class="select select-bordered w-full"
    >
      <option disabled value="">Selecione</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'SelectField',
  props: {
    id: String,
    label: String,
    options: Array,
    modelValue: String,
  },
}
</script>
