<template>
  <v-chip :color="color">
    <p class="text-medium-emphasis">
      <slot name="content"></slot>
    </p>
  </v-chip>
</template>
<script setup>
import {defineProps} from "vue";

const props = defineProps({
  color: String
})
</script>
