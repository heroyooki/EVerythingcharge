<template>
  <v-text-field
    :rules="rules"
    :error="isErrorVisible"
    :error-messages="errorMessage"
    :label="label"
    :required="required"
    density="compact"
    variant="underlined"
    validate-on="input"
    :modelValue="value"
    @update:modelValue="value = $event"
    @input="cleaner"
  ></v-text-field>
</template>

<script setup>
import {defineProps} from "vue";

const props = defineProps({
  rules: Array,
  required: {
    type: Boolean,
    default: false
  },
  label: String,
  isErrorVisible: {
    type: Boolean,
    default: false
  },
  errorMessage: String,
  cleaner: Function,
  value: String
})
</script>
