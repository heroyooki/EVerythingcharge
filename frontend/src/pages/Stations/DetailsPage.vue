<template>
  <station-card>
    <template v-slot:content>
      <!-- Edit button -->
      <aligned-row>
        <template v-slot:left>
          <common-button>
            <template v-slot:content>
              Edit
            </template>
          </common-button>
        </template>
        <!-- Delete button -->
        <template v-slot:right>
          <common-button :color="ELEMENT_COLOR.dangerous_button">
            <template v-slot:content>
              Delete
            </template>
          </common-button>
        </template>
      </aligned-row>
      <v-divider></v-divider>
      <!-- Station details -->
      <station-item-card>
        <template v-slot:id>
          {{ charge_point.id }}
        </template>
        <template v-slot:status>
          {{ charge_point.status }}
        </template>
        <template v-slot:vendor>
          {{ charge_point.vendor }}
        </template>
        <template v-slot:location>
          {{ charge_point.location }}
        </template>
        <template v-slot:description>
          {{ charge_point.description }}
        </template>
      </station-item-card>
      <v-divider></v-divider>
      <!-- Reset button -->
      <aligned-row>
        <template v-slot:center>
          <common-button>
            <template v-slot:content>
              Reset
            </template>
          </common-button>
        </template>
      </aligned-row>
    </template>
  </station-card>

  <v-divider></v-divider>

  <station-card>
    <!-- Tabs with connectors -->
    <template v-slot:content>
      <v-tabs
        :bg-color="ELEMENT_COLOR.tabs"
        v-model="tab"
        align-tabs="center"
      >
        <v-tab
          v-for="connector in charge_point.connectors"
          :value="connector.id"
          class="mdi mdi-connection"
        >connector {{ connector.id }}
        </v-tab>
      </v-tabs>

      <v-card-item>
        <v-window
          v-for="connector in charge_point.connectors"
          v-model="tab"
        >
          <v-window-item :value="connector.id">
            <!-- Connector details -->
            <connector-item-card>
              <template v-slot:status>
                {{ connector.status }}
              </template>
              <template v-slot:error>
                {{ connector.error_code }}
              </template>
            </connector-item-card>
            <!-- Unlock button -->
            <aligned-row>
              <template v-slot:center>
                <common-button>
                  <template v-slot:content>
                    Unlock
                  </template>
                </common-button>
              </template>
            </aligned-row>

          </v-window-item>
        </v-window>
      </v-card-item>
    </template>
  </station-card>
</template>

<script setup>
import {onMounted, ref} from "vue";
import {initScope} from "@/menu/station-menu-items";
import AlignedRow from "@/components/AlignedRow";
import CommonButton from "@/components/CommonButton";
import StationCard from "@/pages/Stations/components/StationCard";
import ConnectorItemCard from "@/pages/Stations/components/ConnectorItemCard";
import StationItemCard from "@/pages/Stations/components/StationItemCard";
import {ELEMENT_COLOR} from "@/enums";

const tab = ref();

const charge_point = {
  id: "0001",
  location: "location",
  vendor: "Vendor",
  model: "Model",
  description: "Description",
  status: "Unavailable",
  connectors: [
    {id: 1, status: "Unavailable", error_code: "NoError"},
    {id: 2, status: "Unavailable", error_code: "NoError"}
  ]
}

onMounted(() => {
  initScope()
})
</script>
