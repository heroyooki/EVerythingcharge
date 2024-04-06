<template>
  <v-btn
    variant="outlined"
    :color="props.color"
    @click="props.onClick"
    :disabled="props.disabled"
    :loading="props.loading"
  >
    <slot name="content"></slot>
  </v-btn>
</template>
<script setup>
import {ELEMENT_COLOR} from "@/enums";
import {defineProps} from "vue";

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  onClick: Function,
  color: {
    type: String,
    default: ELEMENT_COLOR.button
  }
})
</script>
