<template>
  <v-text-field
    :rules="rules"
    :error="isErrorVisible"
    :error-messages="errorMessage"
    :label="label"
    :required="required"
    density="compact"
    variant="underlined"
    validate-on="lazy"
    :modelValue="value"
    @update:modelValue="value = $event"
    @input="cleaner"
  ></v-text-field>
</template>

<script setup>
import {defineProps} from "vue";

const props = defineProps({
  rules: Array,
  required: Boolean,
  label: String,
  isErrorVisible: Boolean,
  errorMessage: String,
  cleaner: Function,
  value: String
})
</script>
