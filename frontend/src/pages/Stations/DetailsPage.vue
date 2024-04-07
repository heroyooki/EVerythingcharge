<template>
  <station-card v-if="item">
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
          {{ item.id }}
        </template>
        <template v-slot:status>
          <text-chip
            :color="STATION_STATUS_COLOR[item.status.toLowerCase()]"
          >
            <template v-slot:content>
              {{ item.status }}
            </template>
          </text-chip>
        </template>
        <template v-slot:vendor>
          {{ item.vendor }}
        </template>
        <template v-slot:location>
          {{ item.location }}
        </template>
        <template v-slot:description>
          {{ item.description }}
        </template>
      </station-item-card>
      <v-divider></v-divider>
      <!-- Reset button -->
      <aligned-row>
        <template v-slot:center>
          <common-button
            :disabled="isForbiddenToReset(item)"
          >
            <template v-slot:content>
              Reset
            </template>
          </common-button>
        </template>
      </aligned-row>
    </template>
  </station-card>

  <v-divider></v-divider>

  <station-card v-if="item.connectors">
    <!-- Tabs with connectors -->
    <template v-slot:content>
      <v-tabs
        :bg-color="ELEMENT_COLOR.tabs"
        v-model="tab"
        align-tabs="center"
      >
        <v-tab
          v-for="connector in item.connectors"
          :value="connector.id"
          class="mdi mdi-connection"
        >connector {{ connector.id }}
        </v-tab>
      </v-tabs>

      <v-card-item>
        <v-window
          v-for="connector in item.connectors"
          v-model="tab"
        >
          <v-window-item :value="connector.id">
            <!-- Connector details -->
            <connector-item-card>
              <template v-slot:status>
                <text-chip
                  :color="STATION_STATUS_COLOR[connector.status.toLowerCase()]"
                >
                  <template v-slot:content>
                    {{ connector.status }}
                  </template>
                </text-chip>
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
import {onMounted, onUnmounted, ref} from "vue";
import {initScope} from "@/menu/station-menu-items";
import TextChip from "@/components/TextChip";
import AlignedRow from "@/components/AlignedRow";
import CommonButton from "@/components/CommonButton";
import StationCard from "@/pages/Stations/components/StationCard";
import ConnectorItemCard from "@/pages/Stations/components/ConnectorItemCard";
import StationItemCard from "@/pages/Stations/components/StationItemCard";
import {ELEMENT_COLOR, STATION_STATUS_COLOR} from "@/enums";
import {getStation} from "@/services/stations";
import {useGetter} from "@/use/getter";
import {useInterval} from "@/use/interval";
import {useRouter} from "vue-router";
import {isForbiddenToReset} from "@/permissions/stations";

const tab = ref();
const router = useRouter();
const stationId = router.currentRoute.value.params.stationId

const {
  item,
  fetchData
} = useGetter({itemsLoader: () => getStation(stationId)})

const {
  fetchWithInterval,
  dropInterval
} = useInterval();


onMounted(() => {
  initScope();
  fetchWithInterval(fetchData);
});

onUnmounted(() => {
  dropInterval();
});
</script>
