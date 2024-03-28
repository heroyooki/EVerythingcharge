export const menuItems = [
  {
    name: "Networks",
    key: "Networks",
    icon: "mdi mdi-lan",
    isVisible: ({currentUser}) => currentUser.is_superuser,
    getPath: () => "/networks",
  },
  {
    name: "Stations",
    key: "Stations",
    icon: "mdi mdi-ev-station",
    isVisible: ({currentNetwork}) => !!currentNetwork,
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}/stations`,
  },
  {
    name: "Transactions",
    key: "Transactions",
    icon: "mdi mdi-battery-charging-high",
    isVisible: ({currentNetwork}) => !!currentNetwork,
    getPath: ({currentNetwork}) => `/${currentNetwork?.id}/transactions`,
  }
];
