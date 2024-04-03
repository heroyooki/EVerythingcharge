<template>
  <data-table
    title="Stations"
    :items="items"
    :headers="headers"
    :current-page="currentPage"
    :last-page="lastPage"
    @page-updated="(newPage) => (currentPage = newPage)"
  >
    <!-- Header -->
    <template v-slot:title="{ title }">
      <table-header>
        <!-- Search input -->
        <template v-slot:search>
          <search-input
            label="Id, Status or Location"
            v-model="search"
          ></search-input>
        </template>
        <!-- Tables's title -->
        <template v-slot:title>
          {{ title }}
        </template>
        <!-- Add new station button-->
        <template v-slot:submit>
          <submit-form :itemSender="addStation"></submit-form>
        </template>
      </table-header>

    </template>
    <!-- Colored station status -->
    <template v-slot:item.status="{ item }">
      <colored-value
        :value="item.columns.status"
        :colorer="STATION_STATUS_COLOR"
      ></colored-value>
    </template>

  </data-table>
</template>

<script setup>
import {onMounted, onUnmounted} from "vue";
import {useStore} from "vuex";
import {dateAgo} from "@/filters/date";
import DataTable from "@/components/DataTable";
import TableHeader from "@/components/TableHeader";
import SearchInput from "@/components/SearchInput";
import ColoredValue from "@/components/ColoredValue";

import {STATION_STATUS_COLOR} from "@/enums";
import {usePagination} from "@/use/pagination";
import {addStation, listStations, streamEndpoint} from "@/services/stations";
import SubmitForm from "@/pages/Stations/components/SubmitForm";

const {commit, getters, dispatch} = useStore();


onMounted(() => {
  dispatch("watchSSE", {
    endpoint: `${getters.currentNetwork.id}/${streamEndpoint}`,
    handler: (data) => items.value = [data, ...items.value.filter(item => item.id !== data.id)]
  });
})

onUnmounted(() => {
  dispatch("closeSSE");
})

const {
  currentPage,
  lastPage,
  items,
  search
} = usePagination({
  itemsLoader: listStations,
});

const headers = [
  {
    title: "Id",
    key: "id",
    align: "right",
    sortable: false,
    width: "20%",
  },
  {
    title: "Version",
    key: "ocpp_version",
    align: "center",
    sortable: false,
    width: "5%",
  },
  {
    title: "Status",
    key: "status",
    align: "center",
    sortable: false,
    width: "10%",
  },
  {
    title: "Location",
    key: "location",
    align: "center",
    sortable: false,
    width: "20%",
  },
  {
    title: "Last activity",
    key: "updated_at",
    align: "center",
    sortable: false,
    value: (v) => dateAgo(v.updated_at),
    width: "15%",
  },
];
</script>
