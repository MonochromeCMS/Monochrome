<template>
  <v-app-bar app flat color="backgroundAlt" :hide-on-scroll="reader">
    <router-link v-if="!settings.title1 && !settings.title2" to="/" class="logo lemon-milk">
      Mono<span class="text--secondary">chrome</span>
    </router-link>
    <router-link v-else to="/" class="logo lemon-milk">
      <span v-if="settings.title1" v-text="settings.title1" />
      <span v-if="settings.title2" v-text="settings.title2" class="text--secondary" />
    </router-link>

    <v-tabs centered class="hidden-sm-and-down" optional v-model="tabs">
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

    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          tile
          color="primary"
          class="hidden-md-and-up ml-auto"
          v-on="on"
          v-bind="attrs"
          aria-label="Navigation menu"
        >
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-tabs vertical>
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
    </v-menu>
  </v-app-bar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AdminActions from '@/components/AdminActions.vue';

@Component({
  components: { AdminActions },
})
export default class NavBar extends Vue {
  tabs = '/';

  links = [
    {
      text: 'Home',
      to: '/',
    },
    {
      text: 'Manga',
      to: '/manga',
    },
    {
      text: 'About',
      to: '/about',
    },
  ];

  drawer = false;

  get reader(): boolean {
    return this.$route.name === 'ChapterReader';
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  get settings(): any {
    return this.$store.getters.settings;
  }
}
</script>

<style lang="scss">
.logo {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: max-content;
  width: calc(100vw - 3rem);
  font-size: 2em;
  text-decoration: none;
}

.login-tab {
  margin-left: auto;
  margin-right: 0 !important;
}
</style>
