<template>
  <v-layout class="h-auto">
    <v-app-bar class="px-3" flat density="compact">
      <v-row justify="end">
      </v-row>
    </v-app-bar>

    <v-navigation-drawer permanent>
      <v-list class="mt-5" density="compact" nav>
        <div v-for="(link, i) in getters.pageMenuItems" :key="i">
          <v-list-item
            :key="link.name"
            :to="link.getPath(getters)"
            :value="link.key"
            :title="link.name"
            :prepend-icon="link.icon"
            :active="isActive(link.key)"
          >
          </v-list-item>
          <v-list-item v-if="link.divider">
            <v-divider></v-divider>
          </v-list-item>
        </div>
      </v-list>
      <v-list density="compact" nav class="logout">
        <v-list-item
          key="logout"
          value="logout"
          title="Logout"
          prepend-icon="mdi mdi-logout"
          @click="store.dispatch('logout')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-3">
      <v-progress-linear
        :indeterminate="getters.globalLoading"
        color="blue-lighten-3"
      ></v-progress-linear>
      <v-container>
        <v-row>
          <v-col md="2">
            <v-sheet>
            </v-sheet>
          </v-col>
          <v-col :md="getters.columnsNumber">
            <v-sheet class="elevation-4 h-screen">
              <router-view></router-view>
            </v-sheet>
          </v-col>
          <v-col md="2">
            <v-sheet>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import {onMounted, ref} from "vue";
import store from "@/store";

const {currentRoute, push} = useRouter();
const {getters, commit} = useStore();

const drawer = ref(true);
const rail = ref(false);

const isActive = (key) => {
  return currentRoute.value.name === key;
};

onMounted(() => {
  const networkId = currentRoute.value.params?.networkId;
  if (networkId) {
    commit("setCurrentNetworkById", networkId);
  }
});
</script>

<style scoped>
.logout {
  position: absolute;
  bottom: 2%;
}
</style>
