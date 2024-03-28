<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar class="px-3" flat density="compact">
      <v-row justify="end">
      </v-row>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
    >
      <v-list-item
        prepend-icon="mdi mdi-land-plots-marker"
        :title="getters.currentUser.first_name"
        nav
      >
        <template v-slot:append>
          <v-btn
            variant="text"
            icon="mdi-chevron-left"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <div v-for="(link, i) in getters.pageMenuItems" :key="i">
          <v-list-item
            v-if="link.isVisible(getters)"
            :key="link.name"
            :to="link.getPath(getters)"
            :value="link.key"
            :title="link.name"
            :prepend-icon="link.icon"
            :active="isActive(link.key)"
            :disabled="!link.isVisible(getters)"
          >
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
          <v-col cols="12" md="9">
            <v-sheet height="90vh" rounded="lg" class="elevation-4">
              <router-view></router-view>
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
  bottom: 30px;
}
</style>
