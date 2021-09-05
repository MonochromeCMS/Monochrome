<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card rounded="lg" color="backgroundAlt" elevation="0">
          <v-card-title class="justify-center lemon-milk">MANGA</v-card-title>
          <manga-page />
          <v-divider v-if="isConnected" />
          <v-card-actions>
            <v-btn
              v-if="isConnected"
              class="my-2 mx-auto"
              to="/manga/new"
              color="background"
            >
              Add a manga
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import MangaPage from "@/components/MangaPage.vue";

@Component({
  components: { MangaPage },
})
export default class Manga extends Vue {
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }
}
</script>
