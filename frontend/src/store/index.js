import {createStore} from "vuex";
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth";
import navigation from "@/store/modules/navigation";
import networks from "@/store/modules/networks";
import layout from "@/store/modules/layout";
import stations from "@/store/modules/stations";
import configurations from "@/store/modules/configurations";

const getDefaultState = () => {
  return {
    loading: false,
  };
};

const state = getDefaultState();

export default createStore({
  state: state,
  mutations: {
    setGlobalLoading(state) {
      state.loading = true;
    },
    unsetGlobalLoading(state) {
      state.loading = false;
    },
  },
  actions: {},
  getters: {
    globalLoading(state) {
      return state.loading;
    },
  },
  modules: {
    auth,
    navigation,
    networks,
    layout,
    stations,
    configurations
  },
  plugins: [
    createPersistedState({
      key: "ocpp.data",
      paths: ["auth", "networks"],
    }),
  ],
});
