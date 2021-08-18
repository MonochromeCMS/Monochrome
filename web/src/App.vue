<template>
  <v-app id="monochrome" class="v-application">
    <nav-bar />
    <v-main class="background">
      <router-view />
    </v-main>
    <theme-toggler />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import NavBar from "./components/NavBar.vue";
import ThemeToggler from "@/components/ThemeToggler.vue";

export default Vue.extend({
  name: "App",

  components: {
    ThemeToggler,
    NavBar,
  },
  computed: {
    isConnected: function () {
      return this.$store.getters.isConnected;
    },
  },
  watch: {
    isConnected: function () {
      this.$router.replace("/");
    },
  },
  mounted() {
    if (this.isConnected) this.$store.dispatch("getUserData");
  },
});
</script>

<style lang="scss">
.v-application {
  font-family: Roboto, serif;
}
</style>
