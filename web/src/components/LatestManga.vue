<template>
  <v-container>
    <v-card-title
      class="justify-center lemon-milk"
      v-text="total <= limit ? 'MANGA' : 'RECENTLY ADDED'"
    />
    <v-row v-if="!loading">
      <v-col class="pt-0">
        <v-list three-line color="backgroundAlt">
          <template v-for="(item, index) in manga">
            <v-divider
              v-if="item.divider"
              :key="index"
              :inset="item.inset"
            ></v-divider>

            <v-list-item v-else :key="item.title" :to="item.to">
              <v-list-item-avatar>
                <v-img :src="item.avatar"></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-html="item.title"></v-list-item-title>
                <v-list-item-subtitle
                  v-html="item.subtitle"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
        <div v-if="manga.length === 0 && alert === ''" class="text-center">
          No manga has been added yet.
        </div>
        <v-alert type="error" v-if="alert !== ''">
          {{ alert }}
        </v-alert>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <v-skeleton-loader
          class="w-100"
          type="list-item-avatar-three-line, divider, list-item-avatar-three-line"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import axios from "axios";
import Vue from "vue";

export default Vue.extend({
  name: "LatestManga",
  data: (): Record<string, any> => ({
    loading: true,
    rawManga: [],
    offset: 0,
    limit: 5,
    alert: "",
    total: 0,
  }),
  computed: {
    manga() {
      let m = this.rawManga
        .map((el: any) => [
          {
            avatar: `/media/${el.id}/cover.jpg?version=${el.version}`,
            title: el.title,
            subtitle: el.description,
            to: `/manga/${el.id}`,
          },
          { divider: true, inset: true },
        ])
        .reduce((acc: [], el: []) => [...acc, ...el], []);

      if (m.length !== 0) m.pop();
      return m;
    },
  },
  methods: {
    async getManga() {
      const url = `/api/manga?limit=${this.limit}&offset=${this.offset}`;
      const response = await axios.get(url);

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
  },
  mounted() {
    this.getManga();
  },
});
</script>
