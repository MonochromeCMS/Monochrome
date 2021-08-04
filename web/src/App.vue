<template>
  <v-app id="monochrome" class="v-application">
    <nav-bar />
    <v-main class="background">
      <router-view />
    </v-main>
    <v-btn
      elevation="3"
      fab
      color="backgroundAlt"
      class="theme-toggle"
      @click="toggleTheme"
    >
      <v-icon large> mdi-lightbulb </v-icon>
    </v-btn>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import NavBar from "./components/NavBar.vue";

export default Vue.extend({
  name: "App",

  components: {
    NavBar,
  },
  methods: {
    toggleTheme: function (): void {
      console.debug(this.$vuetify);
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
  },
  },
});
</script>

<style lang="scss">
.v-application {
  font-family: Roboto, serif;
}

.theme-toggle {
  position: absolute;
  left: 1rem;
  bottom: 1rem;
}
</style>
