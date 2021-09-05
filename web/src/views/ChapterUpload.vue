<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="10" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
          <v-card-title class="justify-center lemon-milk">
            UPLOAD CHAPTER
          </v-card-title>
          <manga-row
            v-if="manga"
            :manga="manga"
            :cover="`/media/${mangaId}/cover.jpg`"
            class="background rounded"
          />
          <v-card-text>
            <upload-form :mangaId="mangaId" />
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
import Manga from "@/api/Manga";

@Component({
  components: { MangaRow, UploadForm },
})
export default class ChapterUpload extends Vue {
  manga = null;
  alert = "";

  get mangaId(): string {
    return this.$route.params.manga;
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  async getManga(): Promise<void> {
    const response = await Manga.get(this.mangaId);

    if (response.data) {
      this.manga = response.data;
    } else {
      this.alert = response.error ?? "";
    }
  }

  mounted(): void {
    if (!this.isConnected) {
      this.$router.replace("/");
    } else {
      this.getManga();
    }
  }
}
</script>
