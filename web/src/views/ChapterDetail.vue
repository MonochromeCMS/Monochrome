<template>
  <v-container fluid class="reader">
    <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
    <v-row v-if="chapter">
      <v-col cols="12" md="8" class="mx-auto" v-if="['Vertical', 'Webtoon'].includes(readerMode)">
        <v-sheet rounded="lg" color="backgroundAlt mx-auto" v-if="chapter">
          <v-row  class="ma-0 pa-3">
            <v-col
                v-bind="columnBind[readerMode]"
                v-for="index in chapter.length - 1"
                :key="index">
              <v-img :src="`/media/${chapter.manga_id}/${chapter_id}/${index+1}.jpg`" />
            </v-col>
          </v-row>
        </v-sheet>
      </v-col>
      <v-col cols="12" v-if="['Single', 'Double'].includes(readerMode)">
        <paged-reader
              :manga="chapter.manga.id"
              :chapter="chapter.id"
              :length="chapter.length"
              :double="readerMode === 'Double'"
              :reverse="!direction"
              @next="goToChapter(nextChapter)"
              @previous="goToChapter(previousChapter)"
          />
      </v-col>
    </v-row>
    <v-dialog max-width="30rem" v-if="chapter" v-model="menu">
      <template v-slot:activator="{ on, attrs }">
        <v-btn fab v-on="on" v-bind="attrs" class="reader-button" color="info">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-card rounded="lg" color="backgroundAlt">
        <v-card-title>
          {{ chapter.manga.title }}
          <v-btn icon class="ml-auto" @click="menu = false"><v-icon>mdi-close</v-icon></v-btn>
        </v-card-title>
        <v-card-text>
          <v-select label="Chapter" hide-details :value="chapter.id" :items="chapterItems" @change="goToChapter"/>
          <v-divider class="mt-3" />
          <v-subheader> Reader settings </v-subheader>
          <v-select label="Reader Mode" hide-details v-model="readerMode" :items="modeItems" />
          <v-row align="center" class="ma-1" v-if="['Single', 'Double'].includes(readerMode)">
            <v-col class="text-body-1">
              Page direction:
            </v-col>
            <v-col class="text-right pa-2">
              <v-btn-toggle v-model="direction" mandatory>
                <v-btn color="background"><v-icon>mdi-arrow-left</v-icon></v-btn>
                <v-btn color="background"><v-icon>mdi-arrow-right</v-icon></v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script type="ts">
import Vue from "vue";
import axios from "axios";
import PagedReader from "@/components/PagedReader.vue";

export default Vue.extend({
  components: {PagedReader},
  data() {return {
    chapter_id: this.$route.params.chapter,
    chapter: null,
    chapters: [],
    menu: false,
    alert: "",
    modeItems: ["Single", "Double", "Vertical", "Webtoon"],
    columnBind: {
      "Single": false,
      "Double": false,
      "Vertical": {
        cols: 12,
      },
      "Webtoon": {
        cols: 12,
        class: "webtoon",
      },
    },
    carouselBind: {
      "Single": true,
      "Double": true,
      "Vertical": false,
      "Webtoon": false,
  }
  }},
  computed: {
    direction: {
      get() {
        return this.$store.getters.getDirection;
      },
      set(value) {
        this.$store.commit("setDirection", value);
      }
    },
    readerMode: {
      get() {
        return this.$store.getters.getReaderMode;
      },
      set(value) {
        this.$store.commit("setReaderMode", value);
      }
    },
    currentChapterIndex() {
      return this.chapters.findIndex(el => el.id === this.chapter_id);
    },
    previousChapter() {
      if (this.currentChapterIndex !== -1 && this.currentChapterIndex < this.chapters.length - 1) {
        return this.chapters[this.currentChapterIndex + 1].id;
      } else {
        return null;
      }
    },
    nextChapter() {
      if (this.currentChapterIndex > 0) {
        return this.chapters[this.currentChapterIndex - 1].id;
      } else {
        return null;
      }
    },
    chapterItems() {
      return this.chapters.map(el => ({
        value: el.id,
        text: this.chapterName(el),
      }));
    }
  },
  methods: {
    async goToChapter(id) {
      if (id) {
        await this.$router.push(`/chapters/${id}`);
        this.chapter_id = id;
        await this.getChapter();
      }
    },
    chapterName(chapter) {
      const volume = chapter.volume ? `Vol ${chapter.volume} ` : "";
      const name = chapter.name ? ` - ${chapter.name}` : "";
      return volume + `Ch ${chapter.number}` + name;
    },
    async getChapter() {
      let url = `/api/chapter/${this.chapter_id}`;

      let response;
      try {
        response = await axios.get(url);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
          this.chapter = response.data;
          this.chapters = [{value: this.chapter_id, text: this.chapterName(response.data)}];
          await this.getChapters(response.data.manga_id);
          break;
        case 404:
          this.alert = "Chapter not found";
          break;
        case 422:
          this.alert = "The ID provided isn't an UUID";
          break;
        default:
          this.alert = response.statusText;
      }
    },
    async getChapters(manga_id) {
      let url = `/api/manga/${manga_id}/chapters`;

      let response;
      try {
        response = await axios.get(url);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
          this.chapters = response.data;
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
    this.getChapter();
  }
});
</script>

<style lang="scss">
.reader {
  .reader-button {
    position: fixed;
    right: 1rem;
    bottom: 1rem;
  }
  .webtoon {
    padding: 0;
  }
}
</style>