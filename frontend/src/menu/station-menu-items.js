import router from "@/router";
import store from "@/store";

export const menuItems = [
  {
    name: "Stations",
    key: "stations",
    icon: "mdi mdi-arrow-left",
    isVisible: () => true,
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}/stations`,
    divider: true
  },
  {
    name: "Details",
    key: "StationsDetails",
    icon: "mdi mdi-ev-station",
    isVisible: () => true,
    getPath: ({
                currentNetwork,
                currentStationId
              }) => `/${currentNetwork?.id}/stations/${currentStationId}`,
  },
  {
    name: "Configuration",
    key: "StationsConfiguration",
    icon: "mdi mdi-hammer-wrench",
    isVisible: () => true,
    getPath: ({
                currentNetwork,
                currentStationId
              }) => `/${currentNetwork?.id}/stations/${currentStationId}/configuration`,
  },
  {
    name: "Charging Profiles",
    key: "ChargingProfiles",
    icon: "mdi mdi-power-settings",
    isVisible: () => true,
    getPath: ({
                currentNetwork,
                currentStationId
              }) => `/${currentNetwork?.id}/stations/${currentStationId}/profiles`,
  }
];

export const initScope = () => {
  store.dispatch("setNarrowLayout");
  store.commit("setPageMenuItems", menuItems);
  store.commit("setCurrentStationId", router.currentRoute.value?.params?.stationId)
}

