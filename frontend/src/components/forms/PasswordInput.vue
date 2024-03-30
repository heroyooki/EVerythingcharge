<template>
  <v-text-field
    :error="isErrorVisible"
    :error-messages="errorMessage"
    type="password"
    label="Password"
    required
    density="compact"
    variant="underlined"
    :modelValue="password"
    @update:modelValue="password = $event"
    @input="cleaner"
  ></v-text-field>
</template>
<script setup>
import {defineProps} from "vue";

const props = defineProps({
  isErrorVisible: Boolean,
  errorMessage: String,
  cleaner: Function,
  password: String
})
</script>
