<template>
  <v-container>
    <v-row align="end" no-gutters>
      <v-col>
        <v-sheet class="pa-2 ma-2">
          <div class="text-center">
            <v-pagination
              :modelValue="currentPage"
              @update:modelValue="updateCurrentPage"
              :length="lastPage"
              total-visible="6"
              density="compact"
            ></v-pagination>
          </div>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row align="start" no-gutters>
      <v-col>
        <v-sheet class="pa-2 ma-2">
          <v-card elevation="0">
            <v-card-title>
              <slot name="title" :title="title">
                <v-card-item class="text-center">{{ title }}</v-card-item>
              </slot>
            </v-card-title>
            <v-data-table
              v-if="items?.length"
              :headers="headers"
              :items="items"
              :hover="props.hover"
              :density="rowConfig.density"
              :class="rowConfig.fontStyle"
              @click:row="onClickRow"
            >
              <template v-for="(_, name) in $slots" #[name]="slotProps">
                <slot :name="name" v-bind="slotProps || {}"></slot>
              </template>
            </v-data-table>
          </v-card>
          <empty-data v-if="!items?.length && !getters.globalLoading"></empty-data>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {useStore} from "vuex";
import {defineEmits, defineProps} from "vue";
import EmptyData from "@/components/EmptyData";

const {getters} = useStore();

const rowConfig = {
  fontStyle: "text-caption",
  density: "comfortable",
};

const props = defineProps({
  hover: {
    type: Boolean,
    default: true,
  },
  headers: Array,
  title: String,
  items: Array,
  currentPage: Number,
  lastPage: Number,
});

const emit = defineEmits(["page-updated", "click-row"]);
const updateCurrentPage = (page) => {
  emit("page-updated", page);
};
const onClickRow = (data, item) => {
  emit("click-row", item);
};
</script>
<style>
.v-data-table-footer {
  display: none;
}
</style>
