const getDefaultState = () => {
  return {
    currentStationId: null
  };
};

const state = getDefaultState();

export default {
  name: "stations",
  state,
  getters: {
    currentStationId(state) {
      return state.currentStationId;
    }
  },
  mutations: {
    setCurrentStationId(state, id) {
      state.currentStationId = id;
    }
  },
};
