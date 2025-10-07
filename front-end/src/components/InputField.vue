<template>
  <div class="form-control">
    <label :for="id" class="label">
      <span class="label-text">{{ label }}</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      required
      class="input input-bordered w-full"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  name: 'InputField',
  props: {
    id: String,
    label: String,
    type: {
      type: String,
      default: 'text',
    },
    modelValue: [String, Number],
  },
}
</script>
