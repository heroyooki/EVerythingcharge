const API_URL = import.meta.env.VITE_API_URL;

const getDefaultState = () => {
  return {
    sseEventSource: null,
    eventType: "message"
  };
};

const state = getDefaultState();

export default {
  name: "sse",
  state,
  actions: {
    watchSSE({commit, state}, {endpoint, handler}) {
      let url = API_URL + `/${endpoint}`;
      let source = new EventSource(url, {withCredentials: true});
      commit("setEventSource", source);

      source.addEventListener(state.eventType, (event) => {
        handler(JSON.parse(event.data));
      });
    },
    closeSSE({state, commit}) {
      state.sseEventSource.close();
      commit("unsetEventSource");
    }
  },
  mutations: {
    setEventSource(state, source) {
      state.sseEventSource = source;
    },
    unsetEventSource(state) {
      state.sseEventSource = null;
    }
  },
};
