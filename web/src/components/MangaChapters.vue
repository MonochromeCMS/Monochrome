<template>
  <v-container>
    <v-row v-if="loading" class="flex-column align-center">
      <v-col cols="12" class="text-h3 text-center" tag="h2"> Chapters </v-col>
      <v-col v-for="i in limit" :key="i">
        <v-row class="justify-space-around background">
          <v-col cols="4" md="3">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-col cols="4" md="4" class="hidden-sm-and-down">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-col cols="4" md="3">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-skeleton-loader type="chip" class="ma-2" />
        </v-row>
      </v-col>
    </v-row>
    <v-row v-else class="flex-column align-center">
      <v-col cols="12" class="text-h3 text-center" tag="h2"> Chapters </v-col>
      <v-col
        cols="12"
        v-for="(item, index) in chaptersPage"
        :key="index"
        class="chapter-row"
      >
        <router-link
          :to="`/manga/${item.manga_id}/${item.id}`"
          class="text-decoration-none"
        >
          <v-row class="justify-space-around background">
            <v-col cols="4" :md="item.volume ? 3 : 2">
              {{ item.volume ? `Vol ${item.volume} ` : "" }}Chapter
              {{ item.number }}
            </v-col>
            <v-col cols="4" md="4" class="hidden-sm-and-down">
              {{ item.name }}
            </v-col>
            <v-col cols="4" md="3">
              {{ item.scan_group }}
            </v-col>
            <v-chip color="backgroundAlt" class="ma-2">
              {{ ago(new Date(item.upload_time).getTime()) }} ago
            </v-chip>
          </v-row>
        </router-link>
      </v-col>
      <v-col cols="12" v-if="pageAmount > 1">
        <v-pagination
          class="mx-auto"
          color="background"
          v-model="page"
          :length="pageAmount"
        ></v-pagination>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  name: "MangaChapters",
  props: ["value", "mangaId"],
  data: () => ({
    chapters: [],
    loading: true,
    limit: 10,
    page: 1,
    innerValue: ["", ""],
  }),
  computed: {
    pageAmount() {
      return Math.ceil(this.chapters.length / this.limit);
    },
    chaptersPage() {
      const start = this.limit * (this.page - 1);
      return this.chapters.slice(start, start + this.limit);
    },
  },
  methods: {
    dispatchValue(error = null, chapter = null) {
      const value = [
        error || this.innerValue[0],
        chapter || this.innerValue[1],
      ];
      this.innerValue = value;
      this.$emit("input", value);
      this.$emit("update:value", value);
    },
    async getChapters() {
      let url = `/api/manga/${this.mangaId}/chapters`;

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
          this.chapters = response.data;
          break;
        case 422:
          this.dispatchValue("The ID provided isn't an UUID");
          break;
        default:
          this.dispatchValue(response.statusText);
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
  watch: {
    chapters() {
      if (this.chapters.length > 0) {
        this.dispatchValue(null, this.chapters[this.chapters.length - 1].id);
      }
    },
  },
  mounted() {
    this.getChapters();
  },
});
</script>

<style lang="scss">
.chapter-row {
  border-bottom: #424242 0.1rem solid;
  &:last-child {
    border-bottom: none;
  }
}
</style>
