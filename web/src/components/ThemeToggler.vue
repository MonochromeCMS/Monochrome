<template>
  <v-btn
    elevation="3"
    fab
    color="backgroundAlt"
    class="theme-toggle"
    @click="toggleTheme"
  >
    <v-icon large> mdi-lightbulb </v-icon>
  </v-btn>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "ThemeToggler",
  methods: {
    toggleTheme: function (): void {
      const dark = !this.$vuetify.theme.dark;
      window.localStorage.setItem("monochrome-dark", dark ? "1" : "0");
      this.$vuetify.theme.dark = dark;
    },
  },
  mounted() {
    this.$vuetify.theme.dark =
      window.localStorage.getItem("monochrome-dark") === "1";
  },
});
</script>

<style lang="scss">
.theme-toggle {
  position: absolute;
  left: 1rem;
  bottom: 1rem;
}
</style>
