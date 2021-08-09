<template>
  <v-container>
    <v-card-title class="justify-center lemon-milk">
      Latest chapters
    </v-card-title>
    <v-row v-if="loading">
      <v-col
        cols="12"
        :lg="isConnected ? 12 : 6"
        xl="6"
        v-for="index in limit"
        :key="index"
        class="my-1"
      >
        <v-card color="background" class="px-4">
          <v-row align="center">
            <v-col cols="3">
              <v-skeleton-loader type="image" />
            </v-col>
            <v-col cols="8">
              <v-skeleton-loader
                class="background chapter-skeleton"
                type="article"
              />
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else class="ma-1">
      <v-col cols="12" v-if="alert !== ''">
        <v-alert type="error">{{ alert }}</v-alert>
      </v-col>
      <v-col
        cols="12"
        class="text-center text-body-1"
        v-else-if="chapters.length === 0"
      >
        No chapters have been uploaded yet.
      </v-col>
      <v-col
        cols="12"
        :lg="isConnected ? 12 : 6"
        xl="6"
        v-for="(chapter, index) in chapters"
        :key="index"
        class="px-1 my-1"
      >
        <v-card
          color="background"
          class="px-4"
          :to="`/chapters/${chapter.id}`"
        >
          <v-row align="center">
            <v-col cols="3">
              <v-img
                :src="`/media/${chapter.manga_id}/cover.jpg`"
                :aspect-ratio="4 / 5"
              />
            </v-col>
            <v-col cols="8" class="d-flex flex-column justify-center">
              <h2 class="text-subtitle-1 ellipsis">
                {{ chapter.manga.title }}
              </h2>
              <h3 class="text-subtitle-2 ellipsis">
                {{
                  `Chapter ${chapter.number}${
                    chapter.name ? " - " + chapter.name : ""
                  }`
                }}
              </h3>
              <h4 class="text-caption">{{ chapter.scan_group }}</h4>
              <v-chip color="backgroundAlt" class="chip-tag">
                {{ ago(new Date(chapter.upload_time).getTime()) }} ago
              </v-chip>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-pagination
        v-if="pageAmount > 1"
        class="mx-auto pb-4"
        color="background"
        v-model="page"
        :length="pageAmount"
      >
      </v-pagination>
    </v-row>
  </v-container>
</template>

<script>
import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  name: "LatestChapters",
  data: () => ({
    page: 1,
    limit: 10,
    total: 0,
    loading: true,
    alert: "",
    chapters: [],
  }),
  computed: {
    pageAmount() {
      return Math.ceil(this.total / this.limit);
    },
    offset() {
      return (this.page - 1) * this.limit;
    },
    isConnected() {
      return this.$store.getters.isConnected;
    },
  },
  methods: {
    async getChapters() {
      let url = `/api/chapter?limit=${this.limit}&offset=${this.offset}`;

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
          this.chapters = response.data.results;
          this.total = response.data.total;
          break;
        default:
          this.alert = response.statusText;
      }

      this.loading = false;
    },
    ago(val) {
      val = 0 | ((Date.now() - val) / 1000);
      const length = {
        second: 60,
        minute: 60,
        hour: 24,
        day: 7,
        week: 4.35,
        month: 12,
        year: 10000,
      };

      for (const unit in length) {
        const result = val % length[unit];
        if (!(val = 0 | (val / length[unit])))
          return result + " " + (result - 1 ? unit + "s" : unit);
      }
    },
  },
  mounted() {
    this.getChapters();
  },
});
</script>

<style lang="scss">
.v-chip.chip-tag {
  margin-top: 0.2rem;
  max-width: max-content;
}
.chapter-skeleton .v-skeleton-loader__article {
  background-color: inherit !important;
}
.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
