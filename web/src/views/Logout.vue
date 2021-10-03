<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk"> LOGOUT </v-card-title>
          <v-card-text> Logging out... </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class Logout extends Vue {
  mounted(): void {
    this.$store.commit('logout');
  }
}
</script>
