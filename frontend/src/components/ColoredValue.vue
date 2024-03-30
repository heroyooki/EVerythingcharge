<template>
  <v-chip
    :color="colorer[value.toLowerCase()]"
  >
    <p class="text-medium-emphasis">
      {{ value }}
    </p>
  </v-chip>
</template>

<script setup>
const props = defineProps({
  colorer: Object,
  value: String
})
</script>
