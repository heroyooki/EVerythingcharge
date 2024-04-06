<template>
  <data-table
    title="Stations"
    :items="items"
    :headers="headers"
    :current-page="currentPage"
    :last-page="lastPage"
    @page-updated="(newPage) => (currentPage = newPage)"
    @click-row="onClickRow"
  >
    <!-- Header -->
    <template v-slot:title="{ title }">
      <aligned-row>
        <!-- Search input -->
        <template v-slot:left>
          <search-input
            label="Id, Status or Location"
            v-model="search"
          ></search-input>
        </template>
        <!-- Tables's title -->
        <template v-slot:center>
          {{ title }}
        </template>
        <!-- Add new station button-->
        <template v-slot:right>
          <submit-form :itemSender="addStation" :callback="fetchData"></submit-form>
        </template>
      </aligned-row>
    </template>
    <!-- Colored ocpp version -->
    <template v-slot:item.ocpp_version="{ item }">
      <colored-value
        :value="item.columns.ocpp_version"
        :colorer="OCPP_VERSION_COLOR"
      ></colored-value>
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
import SearchInput from "@/components/SearchInput";
import ColoredValue from "@/components/ColoredValue";
import AlignedRow from "@/components/AlignedRow";
import router from "@/router";

import {OCPP_VERSION_COLOR, STATION_STATUS_COLOR} from "@/enums";
import {usePagination} from "@/use/pagination";
import {useInterval} from "@/use/interval";
import {addStation, listStations} from "@/services/stations";
import SubmitForm from "@/pages/Stations/components/SubmitForm";
import {initScope} from "@/menu/app-menu-items";

const {commit, getters, dispatch} = useStore();

const {
  currentPage,
  lastPage,
  items,
  search,
  fetchData
} = usePagination({
  itemsLoader: listStations,
});

const {fetchWithInterval, dropInterval} = useInterval();

const onClickRow = ({item}) => {
  router.push({
    name: "StationsDetails",
    params: {stationId: item.value},
  });
}

onMounted(() => {
  initScope();
  fetchWithInterval(fetchData);
});

onUnmounted(() => {
  dropInterval();
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
