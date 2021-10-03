<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="10" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
          <v-card-title class="justify-center lemon-milk"
            >EDIT CHAPTER</v-card-title
          >
          <manga-row
            :loading="!manga"
            :manga="manga"
            :cover="`/media/${manga.id}/cover.jpg`"
            class="background rounded"
          />
          <v-card-text>
            <upload-form
              v-if="chapter && manga"
              :mangaId="manga.id"
              :chapter="chapter"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import MangaRow from "@/components/MangaRow.vue";
import UploadForm from "@/components/UploadForm.vue";
import Chapter, { DetailedChapterResponse } from "@/api/Chapter";
import { MangaResponse } from "@/api/Manga";

@Component({
  components: { MangaRow, UploadForm },
})
export default class About extends Vue {
  manga: MangaResponse | null = null;
  chapter: DetailedChapterResponse | null = null;
  alert = "";

  get chapterId(): string {
    return this.$route.params.chapter;
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  async getChapter(): Promise<void> {
    const response = await Chapter.get(this.chapterId);

    if (response.data) {
      this.chapter = response.data;
      this.manga = response.data.manga;
    } else {
      this.alert = response.error ?? "";
    }
  }

  mounted(): void {
    if (!this.isConnected) {
      this.$router.replace("/");
    } else {
      this.getChapter();
    }
  }
}
</script>
