<template>
  <v-container>

    <v-list lines="two">
      <v-list-item
        v-for="key in Object.keys(configurationSet)"
        :key="key"
        :title="configurationSet[key].verbose"
        :subtitle="key"
      >
        <template v-slot:append>

          <v-switch
            v-if="isBoolean(configurationSet[key].value)"
            disabled
            :model-value="configurationSet[key].value"
            :color="ELEMENT_COLOR.button"
          ></v-switch>

          <v-text-field
            v-else
            disabled
            v-model="configurationSet[key].value"
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
import {onMounted, ref} from "vue";
import {initScope} from "@/menu/station-menu-items";
import {ELEMENT_COLOR} from "@/enums";

const isBoolean = val => !!val === val;

const configurationSet = ref({
  AuthorizeRemoteTxRequests: {
    verbose: 'Enable authorized remote transaction requests',
    value: false,
    name: "authorize_remote_tx_requests"
  },
  StopTransactionOnEVSideDisconnect: {
    verbose: 'Enable stop transaction on EV side disconnect',
    value: true,
    name: "stop_transaction_on_ev_side_disconnect"
  },
  UnlockConnectorOnEVSideDisconnect: {
    verbose: 'Enable unlock connector on EV side disconnect',
    value: true,
    name: "unlock_connector_on_ev_side_disconnect"
  },
  MeterValueSampleInterval: {
    verbose: 'The interval for meter values in seconds',
    value: 60,
    name: "meter_value_sample_interval"
  }
})

onMounted(() => {
  initScope()
})
</script>
