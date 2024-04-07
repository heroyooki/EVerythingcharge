<template>
  <v-card-text>
    <v-container>
      <v-card-subtitle>
        <slot name="status"></slot>
      </v-card-subtitle>
    </v-container>

    <v-container>
      <v-card-subtitle>
        <slot name="error"></slot>
      </v-card-subtitle>
    </v-container>
  </v-card-text>
</template>
<script setup>

</script>
