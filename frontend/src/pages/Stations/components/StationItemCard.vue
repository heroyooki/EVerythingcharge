<template>
  <v-card-item>
    <v-card-title>
      <v-icon class="mdi mdi-ev-station"></v-icon>
      <slot name="id"></slot>
    </v-card-title>
    <v-card-text class="mb-5 mt-5">
      <text-chip :color="props.color">
        <template v-slot:content>
          <slot name="status"></slot>
        </template>
      </text-chip>
      <div>
        <div class="text-h6 mt-5">
          <slot name="vendor"></slot>
        </div>
        <div class="text-overline">
          <slot name="location"></slot>
        </div>
        <div class="text-caption">
          <slot name="description"></slot>
        </div>
      </div>
    </v-card-text>
  </v-card-item>
</template>
<script setup>
import TextChip from "@/components/TextChip";
import {defineProps} from "vue";

const props = defineProps({
  color: String
})
</script>
