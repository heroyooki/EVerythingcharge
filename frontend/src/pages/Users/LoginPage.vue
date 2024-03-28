<template>
  <v-form v-model="isValid">
    <v-container>
      <div align="center" class="mt-16 text-h5 font-weight-light">
        OCPP Management System
      </div>

      <v-row justify="center" class="mt-16">
        <v-card width="600" elevation="15">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" class="mt-10">
                  <v-text-field
                    :error="showError"
                    :error-messages="errors.email"
                    label="Login"
                    required
                    v-model="data.email"
                    density="compact"
                    variant="underlined"
                    validate-on="lazy"
                    @input="clearError"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    type="password"
                    label="Password"
                    required
                    v-model="data.password"
                    density="compact"
                    variant="underlined"
                    validate-on="lazy"
                    @input="clearError"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="mb-7">
            <v-spacer></v-spacer>
            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="onSubmit"
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
import {ref} from "vue";
import store from "@/store";

const loading = ref(false);
const isValid = ref(false);
const data = ref({});
const errors = ref({});
const showError = ref(false);

const onSubmit = () => {
  loading.value = true;
  store
    .dispatch("login", data.value)
    .catch(({response}) => {
      errors.value.email = response?.data?.detail;
    })
    .finally(() => {
      loading.value = false;
    });
};

const clearError = () => {
  showError.value = false;
  errors.value = {};
};
</script>
