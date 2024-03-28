/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";
import { VDataTable } from "vuetify/labs/VDataTable";

// Composables
import { createApp } from "vue";
import { createVuetify } from "vuetify";

// Plugins
import { registerPlugins } from "@/plugins";
import "@mdi/font/css/materialdesignicons.css";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

import router from "@/router";
import store from "@/store";

const vuetify = createVuetify({
  components: {
    VDataTable,
  },
});

const app = createApp(App);
app.component("VueDatePicker", VueDatePicker);
app.use(vuetify);
app.use(store);
app.use(router);

registerPlugins(app);

store
  .dispatch("initAction", {
    isPublicPage: router.currentRoute.meta?.public,
  })
  .then(() => {
    app.mount("#app");
  });
