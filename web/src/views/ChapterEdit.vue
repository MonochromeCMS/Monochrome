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
            v-if="manga"
            :manga="manga"
            :cover="`/media/${manga.id}/cover.jpg`"
            class="background rounded"
          />
          <v-card-text>
            <upload-form
              v-if="chapter"
              :manga_id="manga.id"
              :chapter="chapter"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import axios from "axios";
import MangaRow from "@/components/MangaRow.vue";
import UploadForm from "@/components/UploadForm.vue";

@Component({
  components: { MangaRow, UploadForm },
})
export default class About extends Vue{
  manga = null;
  chapter = null;
  alert = "";

  get chapterId(): string {
    return this.$route.params.chapter;
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  async getChapter(): Promise<void> {
    let url = `/api/chapter/${this.chapterId}`;

    let response;
    try {
      response = await axios.get(url);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 200:
        this.chapter = response.data;
        this.manga = response.data.manga;
        break;
      case 404:
        this.alert = "Chapter not found";
        break;
      case 422:
        this.alert = "The ID provided isn't an UUID";
        break;
      default:
        this.alert = response.data?.detail ?? response.statusText;
    }
  }

  mounted(): void {
    if (!this.isConnected) {
      this.$router.replace("/")
    } else {
      this.getChapter();
    }
  }
}
</script>
