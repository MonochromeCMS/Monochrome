<template>
  <v-container>
    <v-row>
      <v-col>
        <search-bar v-model="search" />
      </v-col>
    </v-row>
    <v-row v-if="loading">
      <v-col cols="12" sm="6" md="4" lg="3" v-for="i in limit" :key="i">
        <v-card color="background" height="100%" class="d-flex flex-column">
          <v-skeleton-loader type="image, article, divider" />
          <v-skeleton-loader type="chip" class="skeleton-chip" />
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col v-if="alert !== ''">
        <v-alert type="error" v-if="alert !== ''">
          {{ alert }}
        </v-alert>
      </v-col>
      <v-col v-else-if="manga.length === 0" class="text-center text-body-1">
        {{
          search ? "No manga could be found." : "No manga has been added yet."
        }}
      </v-col>
      <v-col
        v-else
        cols="12"
        sm="6"
        md="4"
        lg="3"
        v-for="(item, index) in manga"
        :key="index"
      >
        <v-card
          color="background"
          :to="item.to"
          height="100%"
          class="d-flex flex-column"
        >
          <v-img aspect-ratio="1" :src="item.cover"></v-img>
          <v-card-title v-text="item.title" />
          <v-card-subtitle v-text="item.subtitle" />
          <v-card-text
            v-text="item.description"
            class="card-description"
          ></v-card-text>
          <v-divider></v-divider>
          <v-chip
            class="status-chip"
            :color="statusColor[item.status] || 'gray'"
            v-text="upper(item.status)"
          ></v-chip>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="pageAmount > 1">
      <v-pagination
        class="mx-auto pb-4"
        color="background"
        v-model="page"
        :length="pageAmount"
      ></v-pagination>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import axios from "axios";
import Vue from "vue";
import SearchBar from "@/components/SearchBar.vue";

export default Vue.extend({
  name: "MangaPage",
  components: { SearchBar },
  data: (): Record<string, any> => ({
    loading: true,
    rawManga: [],
    limit: 12,
    page: 1,
    alert: "",
    total: 0,
    statusColor: {
      ongoing: "green",
      completed: "green darken-3",
      hiatus: "orange",
      cancelled: "red",
    },
    search: "",
  }),
  computed: {
    manga() {
      return this.rawManga.map((el: any) => ({
        cover: `/media/${el.id}/cover.jpg?version=${el.version}`,
        title: el.title,
        subtitle: el.author,
        description: el.description,
        to: `/manga/${el.id}`,
        status: el.status,
      }));
    },
    offset() {
      return (this.page - 1) * this.limit;
    },
    pageAmount() {
      return Math.ceil(this.total / this.limit);
    },
  },
  methods: {
    async getManga() {
      let url = `/api/manga?limit=${this.limit}&offset=${this.offset}`;
      if (this.search) {
        url += `&title=${this.search}`;
      }

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
          this.rawManga = response.data.results;
          this.total = response.data.total;
          break;
        default:
          this.alert = response.statusText;
      }

      this.loading = false;
    },
    upper(status: string) {
      return status ? status.charAt(0).toUpperCase() + status.slice(1) : "";
    },
  },
  watch: {
    page() {
      this.getManga();
    },
    search() {
      if (this.page === 1) {
        this.getManga();
      } else {
        this.page = 1;
      }
    },
  },
  mounted() {
    if (this.$route.query.q) {
      this.search = this.$route.query.q;
    } else {
      this.getManga();
    }
  },
});
</script>

<style lang="scss">
.status-chip,
.skeleton-chip .v-skeleton-loader__chip {
  margin: 0.5rem 0.5rem 0.5rem auto;
}
.card-description {
  overflow: hidden;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  display: -webkit-box;
  padding-bottom: 0 !important;
  margin-bottom: 1rem;
}
</style>
