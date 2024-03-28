// Composables
import {createRouter, createWebHistory} from "vue-router";
import AuthGuard from "./guards/auth-guard";
import PublicPageGuard from "./guards/public-page-guard";

const routes = [
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
        path: "",
        name: "Dashboard",
        component: () =>
          import(
            /* webpackChunkName: "home" */ "@/pages/DashboardPage.vue"
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
