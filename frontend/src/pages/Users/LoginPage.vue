<template>
  <v-form v-model="isValid">
    <v-container>
      <div align="center" class="text-h5 font-weight-light">
        OCPP Management System
      </div>

      <v-row justify="center" class="mt-16">
        <v-card width="600" elevation="15">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" class="mt-10">
                  <email-input
                    :isErrorVisible="showError && errors.hasOwnProperty('email')"
                    :errorMessage="errors.email"
                    :cleaner="clearError"
                    v-model="data.email"
                  ></email-input>
                </v-col>
                <v-col cols="12">
                  <password-input
                    :isErrorVisible="showError && errors.hasOwnProperty('password')"
                    :errorMessage="errors.password"
                    :cleaner="clearError"
                    v-model="data.password"
                  ></password-input>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="mb-7">
            <v-spacer></v-spacer>
            <v-btn
              :color="ELEMENT_COLOR.button"
              @click="sendData"
              :loading="loading"
              :disabled="!isValid"
            >
              Login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
  </v-form>
</template>
<script setup>
import store from "@/store";
import {useSubmitForm} from "@/use/form";
import EmailInput from "@/components/forms/EmailInput.vue";
import PasswordInput from "@/components/forms/PasswordInput";
import {ELEMENT_COLOR} from "@/enums";

const {
  loading,
  isValid,
  data,
  errors,
  showError,
  clearError,
  sendData,
} = useSubmitForm({
  itemSender: data => store.dispatch("login", data)
});
</script>
