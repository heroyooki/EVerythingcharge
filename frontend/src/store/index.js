import {createStore} from "vuex";
import createPersistedState from "vuex-persistedstate";

import auth from "@/store/modules/auth";
import navigation from "@/store/modules/navigation";
import networks from "@/store/modules/networks";
import sse from "@/store/modules/sse";

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
    sse
  },
  plugins: [
    createPersistedState({
      key: "ocpp.data",
      paths: ["auth", "networks"],
    }),
  ],
});
