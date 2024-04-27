const getDefaultState = () => {
  // Default hardcoded configurations for the station.
  // I gonna use it as is for now.
  // Depending on the business pupropes I will make it configurable.
  return {
    AuthorizeRemoteTxRequests: {
      verbose: 'Enable authorized remote transaction requests',
      value: false,
      key: "authorize_remote_tx_requests"
    },
    StopTransactionOnEVSideDisconnect: {
      verbose: 'Enable stop transaction on EV side disconnect',
      value: true,
      key: "stop_transaction_on_ev_side_disconnect"
    },
    UnlockConnectorOnEVSideDisconnect: {
      verbose: 'Enable unlock connector on EV side disconnect',
      value: true,
      key: "unlock_connector_on_ev_side_disconnect"
    },
    MeterValueSampleInterval: {
      verbose: 'The interval for meter values in seconds',
      value: 60,
      key: "meter_value_sample_interval"
    }
  };
};

const state = getDefaultState();

export default {
  name: "configurations",
  state,
  getters: {
    currentConfigurations(state) {
      return state
    },
    configurationsAsPayload(state) {
      return Object.entries(state)
        .map(([key, item]) => ({key: item.key, value: item.value}));
    }
  }
};
