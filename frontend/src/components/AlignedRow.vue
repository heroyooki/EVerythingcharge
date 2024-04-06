<template>
  <v-container fill-height fluid>
    <v-row no-gutters justify="center">
      <v-col cols="12" sm="4" align="center" v-for="s in slots" :key="s">
        <v-sheet class="ma-2 pa-2">
          <slot :name="s"></slot>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

const slots = ["left", "center", "right"];
</script>
