<template>
  <v-container>
    <v-alert type="error" v-if="alert !== ''">{{ alert }}</v-alert>
    <manga-row :loading="loading" :manga="manga" :cover="cover">
      <div v-if="isConnected || firstChapter">
        <v-btn
          v-if="firstChapter"
          :to="`/manga/${manga.id}/${firstChapter}`"
          color="background"
          max-width="20rem"
          class="mt-5"
        >
          Start reading
        </v-btn>
        <v-btn
          v-if="isConnected"
          :to="`/manga/${mangaId}/upload`"
          color="background"
          max-width="20rem"
          class="mt-5 ml-5"
        >
          Add chapter
        </v-btn>
      </div>
    </manga-row>
    <manga-chapters :manga-id="mangaId" v-model="chapterModel" />
  </v-container>
</template>

<script lang="ts">
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
    };
  },
  mounted() {
    this.getManga();
  },
  computed: {
    cover() {
      return `/media/${this.mangaId}/cover.jpg`;
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
  },
});
</script>
