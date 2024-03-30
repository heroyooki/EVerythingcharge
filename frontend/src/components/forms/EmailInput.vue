<template>
  <v-text-field
    :rules="rules"
    :error="isErrorVisible"
    :error-messages="errorMessage"
    label="Email"
    required
    density="compact"
    variant="underlined"
    validate-on="lazy blur"
    :modelValue="email"
    @update:modelValue="email = $event"
    @input="cleaner"
  ></v-text-field>
</template>

<script setup>
import {defineProps} from "vue";

const rules = [
  value => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!re.test(String(value).toLowerCase())) {
      return "Please enter a valid email address";
    }
    return true;
  }
]

const props = defineProps({
  isErrorVisible: Boolean,
  errorMessage: String,
  cleaner: Function,
  email: String
})
</script>
