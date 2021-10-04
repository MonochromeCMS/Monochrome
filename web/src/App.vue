<template>
  <v-app id="monochrome" class="v-application">
    <nav-bar />
    <v-main class="background">
      <router-view />
    </v-main>
    <notifications />
    <theme-toggler />
  </v-app>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import NavBar from '@/components/NavBar.vue';
import Notifications from '@/components/Notifications.vue';
import ThemeToggler from '@/components/ThemeToggler.vue';

@Component({
  components: {
    ThemeToggler,
    NavBar,
    Notifications,
  },
})
export default class App extends Vue {
  get isConnected() {
    return this.$store.getters.isConnected;
  }

  @Watch('isConnected')
  onLoginChange() {
    this.$router.replace('/');
  }

  mounted() {
    if (this.isConnected) this.$store.dispatch('getUserData');
    this.$store.dispatch('getSettings');
  }
}
</script>

<style lang="scss">
.v-application {
  font-family: Roboto, serif;
}
</style>
