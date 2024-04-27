<template>
  <v-container>

    <v-list lines="two">
      <v-list-item
        v-for="key in Object.keys(getters.currentConfigurations)"
        :key="key"
        :title="getters.currentConfigurations[key].verbose"
        :subtitle="key"
      >
        <template v-slot:append>

          <v-switch
            v-if="isBoolean(getters.currentConfigurations[key].value)"
            disabled
            :model-value="getters.currentConfigurations[key].value"
            :color="ELEMENT_COLOR.button"
          ></v-switch>

          <v-text-field
            v-else
            disabled
            v-model="getters.currentConfigurations[key].value"
            hide-details
            single-line
            variant="outlined"
            style="width: 60px"
            density="compact"
          ></v-text-field>

        </template>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script setup>
import {onMounted} from "vue";
import {initScope} from "@/menu/station-menu-items";
import {ELEMENT_COLOR} from "@/enums";
import {useStore} from "vuex";

const {getters} = useStore();

const isBoolean = val => !!val === val;

onMounted(() => {
  initScope()
})
</script>
