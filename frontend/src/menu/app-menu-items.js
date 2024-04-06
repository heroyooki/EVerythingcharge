import store from "@/store";

export const menuItems = [
  {
    name: "Dashboard",
    key: "Dashboard",
    icon: "mdi mdi-monitor-dashboard",
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}`,
  },
  {
    name: "Stations",
    key: "Stations",
    icon: "mdi mdi-ev-station",
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}/stations`,
  },
  {
    name: "Transactions",
    key: "Transactions",
    icon: "mdi mdi-battery-charging-high",
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}/transactions`,
  }
];

export const initScope = () => {
  store.dispatch("setBroadLayout");
  store.commit("setPageMenuItems", menuItems);
}
