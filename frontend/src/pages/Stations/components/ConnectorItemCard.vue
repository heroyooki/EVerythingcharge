<template>
  <v-card-text>
    <v-container>
      <v-card-subtitle>
        <text-chip :color="props.color">
          <template v-slot:content>
            <slot name="status"></slot>
          </template>
        </text-chip>
      </v-card-subtitle>
    </v-container>

    <v-container>
      <v-card-subtitle>
        <text-chip :color="props.color">
          <template v-slot:content>
            <slot name="error"></slot>
          </template>
        </text-chip>
      </v-card-subtitle>
    </v-container>
  </v-card-text>
</template>
<script setup>
import TextChip from "@/components/TextChip";
import {defineProps} from "vue";

const props = defineProps({
  color: String
})
</script>
