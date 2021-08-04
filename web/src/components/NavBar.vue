<template>
  <v-app-bar app flat color="backgroundAlt">
    <router-link to="/" class="logo">
      Mono<span class="text--secondary">chrome</span>
    </router-link>

    <v-tabs centered class="ml-n9">
      <v-tab v-for="link in links" :key="link.text" :to="link.to">
        {{ link.text }}
      </v-tab>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "NavBar",

  data: (): Record<string, any> => ({
    links: [
      {
        text: "Home",
        to: "/",
      },
      {
        text: "Manga",
        to: "/manga",
      },
      {
        text: "About",
        to: "/about",
      },
    ],
  }),
});
</script>

<style lang="scss">
.logo {
  font-family: LemonMilk, Roboto, serif;
  font-size: 2em;
  text-decoration: none;
}

.login-tab {
  margin-left: auto;
  margin-right: 0 !important;
}
</style>
