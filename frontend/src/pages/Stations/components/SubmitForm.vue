<template>

  <v-btn
    :color="ELEMENT_COLOR.button"
    @click="openModal">
    add
  </v-btn>

  <v-form v-model="isValid">
    <v-container>
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="600">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <text-input
                      :rules="validationRules.id"
                      :isErrorVisible="showError && !!errors.id"
                      :errorMessage="errors.id"
                      label="Id"
                      required
                      v-model="data.id"
                      :cleaner="clearError"
                    ></text-input>
                  </v-col>
                  <v-col cols="12">
                    <text-input
                      :rules="validationRules.location"
                      required
                      label="Location"
                      v-model="data.location"
                    ></text-input>
                  </v-col>
                  <v-col cols="12">
                    <text-input
                      :rules="validationRules.description"
                      label="Description"
                      v-model="data.description"
                    ></text-input>
                  </v-col>
                  <v-col cols="12">
                    <text-input
                      :rules="validationRules.ocpp_version"
                      label="OCPP Version"
                      v-model="data.ocpp_version"
                    ></text-input>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="mb-7">
              <v-spacer></v-spacer>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="closeModal"
                :disabled="loading"
              >
                Close
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="sendData"
                :loading="loading"
              >
                Add
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
  </v-form>
</template>

<script setup>
import {useSubmitForm} from "@/use/form";
import {ELEMENT_COLOR} from "@/enums";
import TextInput from "@/components/forms/TextInput";
import {validationRules} from "@/pages/Stations/validators";

const props = defineProps({
  itemSender: Function
})
const {
  loading,
  isValid,
  dialog,
  data,
  errors,
  showError,
  clearError,
  openModal,
  closeModal,
  sendData,
} = useSubmitForm({
  itemSender: props.itemSender
});
</script>
