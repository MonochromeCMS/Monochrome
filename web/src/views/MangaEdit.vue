<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10" md="8" lg="6" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk"> EDIT MANGA </v-card-title>
          <v-card-text>
            <manga-form v-if="manga" :manga="manga" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import MangaForm from '@/components/MangaForm.vue';
import type { MangaResponse } from '@/api/Manga';
import Manga from '@/api/Manga';

@Component({
  components: { MangaForm },
})
export default class MangaEdit extends Vue {
  manga: MangaResponse | null = null;

  get id(): string {
    return this.$route.params.manga;
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  async getManga(): Promise<void> {
    const response = await Manga.get(this.id);

    if (response.data) {
      this.manga = response.data;
    } else {
      const notification = {
        context: 'Get manga',
        message: response.error ?? '',
        color: 'error',
      };
      this.$store.commit('addNotification', notification);
    }
  }

  mounted(): void {
    if (!this.isConnected) {
      this.$router.replace('/');
    } else {
      this.getManga();
    }
  }
}
</script>
