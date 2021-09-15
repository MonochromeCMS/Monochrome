<template>
  <v-container>
    <v-row>
      <v-col>
        <v-sheet rounded="lg" color="backgroundAlt">
          <v-container>
            <v-alert type="error" v-if="alert !== ''">{{ alert }}</v-alert>
            <manga-row :loading="loading" :manga="manga" :cover="cover">
              <div v-if="isConnected || firstChapter" class="d-flex flex-wrap">
                <v-btn
                  v-if="firstChapter"
                  :to="`/chapters/${firstChapter}`"
                  color="background"
                  class="ma-2"
                >
                  Start reading
                </v-btn>
                <v-btn
                  v-if="isConnected"
                  :to="`/manga/${mangaId}/upload`"
                  color="green darken-2"
                  class="ma-2"
                >
                  Add chapter
                </v-btn>
                <v-btn
                  v-if="isConnected"
                  :to="`/manga/${mangaId}/edit`"
                  color="info"
                  class="ma-2"
                >
                  Edit manga
                </v-btn>
                <v-dialog
                  v-if="isConnected"
                  v-model="deleteDialog"
                  max-width="30rem"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn color="error" v-bind="attrs" v-on="on" class="ma-2">
                      Delete manga
                    </v-btn>
                  </template>

                  <v-card>
                    <v-card-title class="text-h5 background mb-2">
                      Warning
                    </v-card-title>

                    <v-card-text class="body-1">
                      <span class="font-weight-bold"
                        >This action can't be undone!</span
                      >
                      Are you sure you want to delete this manga?
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="gray" text @click="deleteDialog = false">
                        Cancel
                      </v-btn>
                      <v-btn color="error" @click="deleteManga"> Delete </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </div>
            </manga-row>
            <manga-chapters :manga-id="mangaId" v-model="chapterModel" />
          </v-container>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import type { AxiosRequestConfig } from "axios";
import MangaRow from "@/components/MangaRow.vue";
import MangaChapters from "@/components/MangaChapters.vue";
import Manga, { MangaResponse } from "@/api/Manga";

@Component({
  components: { MangaChapters, MangaRow },
})
export default class MangaDetail extends Vue {
  manga: MangaResponse | null = null;
  loading = true;
  mangaAlert = "";
  chapterModel = ["", ""];
  deleteDialog = false;

  get mangaId(): string {
    return this.$route.params.manga;
  }

  get cover(): string | null {
    if (this.manga) {
      return `/media/${this.manga?.id}/cover.jpg?version=${this.manga?.version}`;
    }
    return null;
  }

  get alert(): string {
    return this.mangaAlert || this.chapterModel[0];
  }

  get firstChapter(): any {
    return this.chapterModel[1];
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  async getManga(): Promise<void> {
    const response = await Manga.get(this.mangaId, this.loading);

    if (response.data) {
      this.manga = response.data;
    } else {
      this.mangaAlert = response.error ?? "";
    }

    this.loading = false;
  }

  async deleteManga(): Promise<void> {
    const config = this.authConfig;
    const response = await Manga.delete(this.mangaId, config);

    if (response.data || response.status === 404) {
      await this.$router.push("/manga");
    } else {
      this.mangaAlert = response.error ?? "";
    }
    if (response.status === 401) {
      this.$store.commit("logout");
    }

    this.deleteDialog = false;
  }

  mounted(): void {
    this.getManga();
  }
}
</script>
