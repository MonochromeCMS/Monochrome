<template>
  <v-btn fab outlined color="primary" class="theme-toggle" @click="toggleTheme" aria-hidden="true">
    <v-icon large> mdi-lightbulb </v-icon>
  </v-btn>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class ThemeToggler extends Vue {
  toggleTheme(): void {
    const dark = !this.$vuetify.theme.dark;
    window.localStorage.setItem('monochrome-dark', dark ? '1' : '0');
    this.$vuetify.theme.dark = dark;
  }

  mounted(): void {
    this.$vuetify.theme.dark = window.localStorage.getItem('monochrome-dark') === '1';
  }
}
</script>

<style lang="scss">
.theme-toggle {
  position: fixed;
  left: 1rem;
  bottom: 1rem;
}
</style>
