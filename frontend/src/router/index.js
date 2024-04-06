// Composables
import {createRouter, createWebHistory} from "vue-router";
import AuthGuard from "./guards/auth-guard";
import HomePageGuard from "@/router/guards/home-page-guard";
import PublicPageGuard from "./guards/public-page-guard";

const routes = [
  {
    path: "/",
    name: "Home",
    redirect: HomePageGuard
  },
  {
    path: "/404",
    name: "404",
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/NotFoundPage.vue"),
  },
  {
    path: "/login",
    name: "Login",
    beforeEnter: PublicPageGuard,
    component: () =>
      import(/* webpackChunkName: "home" */ "@/pages/Users/LoginPage.vue"),
    meta: {
      public: true,
    },
  },
  {
    path: "/",
    component: () => import("@/layouts/AppLayout.vue"),
    beforeEnter: AuthGuard,
    children: [
      {
        path: ":networkId",
        name: "Dashboard",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/DashboardPage.vue"
            ),
      },
      {
        path: ":networkId/stations",
        name: "Stations",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/ListPage.vue"
            ),
      },
      {
        path: ":networkId/stations/:stationId",
        name: "StationsDetails",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/DetailsPage.vue"
            ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":networkId/stations/:stationId/configuration",
        name: "StationsConfiguration",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/ConfigurationPage.vue"
            ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":networkId/stations/:stationId/profiles",
        name: "ChargingProfiles",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Stations/ChargingProfilesPage.vue"
            ),
        meta: {
          hasBackButton: true,
        },
      },
      {
        path: ":networkId/transactions",
        name: "Transactions",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/Transactions/ListPage.vue"
            ),
      }
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
