import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/manga",
    name: "Manga",
    component: () =>
      import(/* webpackChunkName: "manga" */ "../views/Manga.vue"),
  },
  {
    path: "/manga/new",
    name: "MangaCreate",
    component: () =>
      import(/* webpackChunkName: "manga_create" */ "../views/MangaCreate.vue"),
  },
  {
    path: "/manga/:manga",
    name: "MangaDetail",
    component: () =>
      import(/* webpackChunkName: "manga_detail" */ "../views/MangaDetail.vue"),
  },
  {
    path: "/manga/:manga/edit",
    name: "MangaEdit",
    component: () =>
      import(/* webpackChunkName: "manga_edit" */ "../views/MangaEdit.vue"),
  },
  {
    path: "/manga/:manga/upload",
    name: "ChapterUpload",
    component: () =>
      import(/* webpackChunkName: "chapter_upload" */ "../views/ChapterUpload.vue"),
  },
  {
    path: "/manga/:manga/:chapter/upload",
    name: "ChapterEdit",
    component: () =>
      import(/* webpackChunkName: "chapter_edit" */ "../views/ChapterEdit.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/logout",
    name: "Logout",
    component: () =>
      import(/* webpackChunkName: "logout" */ "../views/Logout.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/",
    name: "Home",
    component: () => import(/* webpackChunkName: "home" */ "../views/Home.vue"),
  },
  {
    path: "*",
    redirect: "/",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
