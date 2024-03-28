const getDefaultState = () => {
  return {
    pageMenuItems: [],
    prevPage: "",
    pageHasBackButton: false,
  };
};

const state = getDefaultState();

export default {
  name: "navigation",
  state,
  actions: {
    storeMenuItems({ commit }, menuItems) {
      commit("setPageMenuItems", menuItems);
    },

    storePrevPage({ commit }, url) {
      commit("setPrevPage", url);
    },

    storePageHasBackButton({ commit }, flag) {
      commit("setPageHasBackButton", flag);
    },
  },

  getters: {
    pageMenuItems(state) {
      return state.pageMenuItems;
    },

    prevPage(state) {
      return state.prevPage && state.pageHasBackButton ? state.prevPage : "";
    },

    pageHasBackButton(state) {
      return state.pageHasBackButton;
    },
  },

  mutations: {
    setPageMenuItems(state, items) {
      state.pageMenuItems = items;
    },

    setPrevPage(state, url) {
      state.prevPage = url;
    },

    setPageHasBackButton(state, flag) {
      state.pageHasBackButton = flag;
    },

    setMiniSideBar(state, value) {
      state.miniSideBar = value;
    },
  },
};
