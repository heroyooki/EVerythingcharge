<template>

  <common-button :onClick="openModal">
    <template v-slot:content>
      Add
    </template>
  </common-button>

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

              <common-button
                :onClick="closeModal"
                :disabled="loading"
              >
                <template v-slot:content>
                  Close
                </template>
              </common-button>

              <common-button
                :onClick="sendData"
                :loading="loading"
                :disabled="!isValid || loading"
              >
                <template v-slot:content>
                  Submit
                </template>
              </common-button>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-container>
  </v-form>
</template>

<script setup>
import {useSubmitForm} from "@/use/form";
import TextInput from "@/components/forms/TextInput";
import CommonButton from "@/components/CommonButton"
import {validationRules} from "@/pages/Stations/validators";

const props = defineProps({
  itemSender: Function,
  callback: Function
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
  itemSender: props.itemSender,
  callback: props.callback
});
</script>
