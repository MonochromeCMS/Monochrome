<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="10" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
          <v-card-title class="justify-center lemon-milk">
            UPLOAD CHAPTER
          </v-card-title>
          <manga-row v-if="manga" :manga="manga" :cover="`/media/${manga_id}/cover.jpg`" class="background rounded" />
          <v-card-text>
            <upload-form :manga_id="manga_id" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script type="ts">
import Vue from "vue";
import axios from "axios";
import MangaRow from "@/components/MangaRow.vue";
import UploadForm from "@/components/UploadForm.vue";

export default Vue.extend({
  components: {UploadForm, MangaRow},
  data() {return {
    manga: null,
    manga_id: this.$route.params.manga,
    alert: "",
  }},
  computed: {
    isConnected() {
      return this.$store.getters.isConnected;
    },
  },
  methods: {
    async getManga() {
      let url = `/api/manga/${this.manga_id}`;

      let response;
      try {
        response = await axios.get(url);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
          this.manga = response.data;
          break;
        case 404:
          this.alert = "Manga not found";
          break;
        case 422:
          this.alert = "The ID provided isn't an UUID";
          break;
        default:
          this.alert = response.statusText;
      }
    },
  },
  mounted() {
    if (!this.isConnected) {
      this.$router.replace("/")
    } else {
      this.getManga();
    }
  },
});
</script>
