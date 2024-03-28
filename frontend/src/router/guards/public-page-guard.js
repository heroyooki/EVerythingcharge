import store from "@/store"; // We need to import store like this here

export default (to, from, next) => {
  // Go to Dashboard if authorized user tries to reach public pages
  if (store.getters.isAuthorized) {
    next("/");
  } else {
    next();
  }
};
