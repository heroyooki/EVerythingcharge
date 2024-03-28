import router from "@/router";
import {request} from "@/api";

const getDefaultState = () => {
  return {
    isAuthorized: false,
    user: {
      is_superuser: false,
    },
  };
};

const state = getDefaultState();

function _processSuccessfulLogout(commit) {
  commit("unsetAuthorized");
  commit("unsetUser");
  commit("unsetCurrentNetwork");
  router.push("/login");
}

export default {
  name: "auth",
  state,
  actions: {
    initAction({getters}, payload) {
      // We don't want to make unnecessary request to the backend in case it's
      // a public page, it may effect Page Load Time
      if (!payload.isPublicPage && getters.isAuthorized) {
        this.dispatch("getUser").catch(() => {
          console.log("Wasn't able to receive user data");
        });
      } else {
        return Promise.resolve();
      }
    },
    getUser({commit}) {
      return request.get("/me").then((user) => {
        commit("setUser", user);
        commit("setNetworks", user?.networks);
        commit("setCurrentNetwork", user?.networks);
      });
    },

    silentLogout({commit}) {
      _processSuccessfulLogout(commit);
    },

    logout() {
      request.delete("/logout");
    },

    login({commit}, credentials) {
      return request.post("/login", credentials).then(() => {
        this.dispatch("getUser").then(() => {
          commit("setAuthorized");
          router.push("/");
        })
      });
    },
  },
  getters: {
    currentUser(state) {
      return state.user;
    },

    isAuthorized(state) {
      return state.isAuthorized;
    },
  },

  mutations: {
    setAuthorized(state) {
      state.isAuthorized = true;
    },

    unsetAuthorized(state) {
      state.isAuthorized = false;
    },

    setUser(state, data) {
      state.user = data;
    },

    unsetUser(state) {
      state.user = {};
    },

    unsetNetworks(state) {
      state.networks = [];
    },
  },
};
