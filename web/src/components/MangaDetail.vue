<template>
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
          color="background"
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
        <v-dialog v-if="isConnected" v-model="deleteDialog" max-width="30rem">
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
              <span class="font-weight-bold">This action can't be undone!</span>
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
</template>

<script>
import Vue from "vue";
import axios from "axios";
import MangaChapters from "@/components/MangaChapters.vue";
import MangaRow from "@/components/MangaRow.vue";

export default Vue.extend({
  name: "MangaDetail",
  components: { MangaRow, MangaChapters },
  data() {
    return {
      mangaId: this.$route.params.manga,
      manga: {},
      loading: true,
      mangaAlert: "",
      chapterModel: ["", ""],
      deleteDialog: false,
    };
  },
  mounted() {
    this.getManga();
  },
  computed: {
    cover() {
      return `/media/${this.mangaId}/cover.jpg?version=${this.manga.version}`;
    },
    alert() {
      return this.mangaAlert || this.chapterModel[0];
    },
    firstChapter() {
      return this.chapterModel[1];
    },
    isConnected() {
      return this.$store.getters.isConnected;
    },
    authConfig() {
      return this.$store.getters.authConfig;
    },
  },
  methods: {
    async getManga() {
      let url = `/api/manga/${this.mangaId}`;

      let response;
      try {
        response = await axios.get(url);
      } catch (e) {
        response = e.response;
      }

      if (this.loading) {
        await new Promise((resolve) => {
          setTimeout(() => resolve("done!"), 500);
        });
      }

      switch (response.status) {
        case 200:
          this.manga = response.data;
          break;
        case 404:
          this.mangaAlert = "Manga not found";
          break;
        case 422:
          this.mangaAlert = "The ID provided isn't an UUID";
          break;
        default:
          this.mangaAlert = response.statusText;
      }

      this.loading = false;
    },
    async deleteManga() {
      const config = this.authConfig;

      let url = `/api/manga/${this.mangaId}`;

      let response;
      try {
        response = await axios.delete(url, config);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
        case 404:
          await this.$router.push("/manga");
          break;
        case 401:
          this.$store.commit("logout");
          break;
        case 422:
          this.mangaAlert = "The ID provided isn't an UUID";
          break;
        default:
          this.mangaAlert = response.statusText;
      }

      this.deleteDialog = false;
    },
  },
});
</script>
