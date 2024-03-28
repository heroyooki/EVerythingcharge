const getDefaultState = () => {
  return {
    networks: [],
    currentNetwork: null,
  };
};

const state = getDefaultState();

export default {
  name: "networks",
  state,
  actions: {},
  getters: {
    currentNetwork(state) {
      return state.currentNetwork;
    },
    dropDownList(state) {
      return state.networks.filter((item) => item.id !== state.currentNetwork.id);
    },
  },
  mutations: {
    setCurrentNetwork(state, networks) {
      if (networks.length) {
        state.currentNetwork = networks[0];
      }
    },
    setCurrentNetworkById(state, networkId) {
      state.currentNetwork = state.networks.filter(
        (item) => item.id === networkId
      )[0];
    },
    unsetCurrentNetwork(state) {
      state.currentNetwork = null;
    },
    setNetworks(state, networks) {
      state.networks = networks;
    },
    unsetNetworks(state) {
      state.networks = [];
    },
  },
};
