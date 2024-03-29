import store from "@/store"; // We need to import store like this here

export default () => {
  // Go to Dashboard or Login page from root path
  const path = `/${store.getters.currentNetwork?.id}`;
  return store.getters.isAuthorized ? path : "/login";
};
