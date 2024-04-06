const getDefaultState = () => {
  return {
    columnsNumber: 12
  };
};

const state = getDefaultState();

export default {
  name: "layout",
  state,
  actions: {
    setBroadLayout({commit}) {
      commit("setColumnsNumber", 12);
    },
    setNarrowLayout({commit}) {
      commit("setColumnsNumber", 7);
    },
  },
  getters: {
    columnsNumber(state) {
      return state.columnsNumber;
    }
  },
  mutations: {
    setColumnsNumber(state, items) {
      state.columnsNumber = items;
    }
  },
};
