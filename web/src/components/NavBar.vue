<template>
  <v-app-bar app flat color="backgroundAlt">
    <router-link to="/" class="logo lemon-milk">
      Mono<span class="text--secondary">chrome</span>
    </router-link>

    <v-tabs centered class="ml-n9">
      <v-tab v-for="link in links" :key="link.text" :to="link.to">
        {{ link.text }}
      </v-tab>
      <v-tab v-if="!isConnected" to="/login" class="login-tab"> Login </v-tab>
      <v-menu v-else offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-tab v-on="on" v-bind="attrs" class="login-tab"> Admin </v-tab>
        </template>

        <admin-actions :left="true" />
      </v-menu>
    </v-tabs>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import AdminActions from "@/components/AdminActions.vue";

export default Vue.extend({
  name: "NavBar",
  components: { AdminActions },
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
  computed: {
    isConnected: function () {
      return this.$store.getters.isConnected;
    },
  },
});
</script>

<style lang="scss">
.logo {
  font-size: 2em;
  text-decoration: none;
}

.login-tab {
  margin-left: auto;
  margin-right: 0 !important;
}
</style>
