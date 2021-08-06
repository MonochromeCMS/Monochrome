<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card rounded="lg" color="backgroundAlt" elevation="0">
          <v-card-title class="justify-center lemon-milk">MANGA</v-card-title>
          <manga-page />
          <v-divider v-if="isConnected" />
          <v-card-actions>
            <v-btn v-if="isConnected" class="my-2 mx-auto" to="/manga/new"
              >Add a manga</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import Vue from "vue";
import MangaPage from "../components/MangaPage";
export default Vue.extend({
  components: { MangaPage },
  computed: {
    isConnected() {
      return this.$store.getters.isConnected;
    },
  },
});
</script>
