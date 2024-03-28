<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent width="auto">
      <v-card>
        <v-card-title class="text-center">
          You can not discard this action.
        </v-card-title>
        <v-card-text class="text-center"> Are you sure?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeConfirm()">
            No
          </v-btn>
          <v-btn
            color="red"
            variant="text"
            :loading="loading"
            @click="fetchAction()"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script setup>
import { defineProps, ref } from "vue";
import { useConfirm } from "@/use/dialogs";

const props = defineProps(["callback"]);
const loading = ref(false);

const fetchAction = () => {
  loading.value = true;
  props
    .callback()
    .then(() => {
      closeConfirm();
    })
    .finally(() => {
      loading.value = false;
    });
};

const { dialog, closeConfirm } = useConfirm();
</script>
