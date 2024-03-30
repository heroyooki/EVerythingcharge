<template>
  <v-text-field
    :label="label"
    density="compact"
    variant="outlined"
    append-inner-icon="mdi-magnify"
    :modelValue="search"
    @update:modelValue="search = $event"
  >
  </v-text-field>
</template>

<script setup>
import {defineProps} from "vue";

const props = defineProps({
  label: String,
  search: String
});
</script>
