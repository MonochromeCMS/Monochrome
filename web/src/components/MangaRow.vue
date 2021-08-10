<template>
  <v-container>
    <v-row v-if="loading" align="center">
      <v-col cols="3">
        <v-skeleton-loader type="image" />
      </v-col>
      <v-col cols="9" class="d-flex flex-column justify-center">
        <v-skeleton-loader type="heading" class="mb" />
        <v-skeleton-loader
          type="chip, chip, chip"
          class="d-flex flex-wrap skeleton-tag"
        />
        <v-skeleton-loader type="text@3" class="mr-5" />
        <v-skeleton-loader type="button" />
      </v-col>
    </v-row>
    <v-row v-else align="center">
      <v-col cols="12" sm="3">
        <v-img :src="cover" contain />
      </v-col>
      <v-col cols="12" sm="9" class="d-flex flex-column justify-center">
        <v-tooltip top open-delay="600">
          <template v-slot:activator="{ on, attrs }">
            <h1 class="text-h2 pb-2 ellipsis" v-bind="attrs" v-on="on">
              {{ manga.title }}
            </h1>
          </template>
          <span v-text="manga.title" />
        </v-tooltip>
        <div class="d-flex flex-wrap">
          <v-chip
            class="chip-tag"
            :color="statusColor[manga.status] || 'gray'"
            v-text="upper(manga.status)"
          ></v-chip>
          <v-chip class="chip-tag" color="background">
            <span>Author: </span> {{ manga.author }}
          </v-chip>
          <v-chip class="chip-tag" color="background">
            <span>Artist: </span> {{ manga.artist }}
          </v-chip>
          <v-chip v-if="manga.year" class="chip-tag" color="background">
            <span>Release: </span> {{ manga.year }}
          </v-chip>
        </div>
        <div class="manga-desc">{{ manga.description }}</div>
        <slot></slot>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "MangaRow",
  props: ["manga", "cover", "loading"],
  data: () => ({
    statusColor: {
      ongoing: "green",
      completed: "green darken-3",
      hiatus: "orange",
      cancelled: "red",
    },
  }),
  methods: {
    upper(status: string) {
      return status ? status.charAt(0).toUpperCase() + status.slice(1) : "";
    },
  },
});
</script>

<style lang="scss">
.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.manga-desc {
  margin: 0.5rem;
  font-weight: 400;
  letter-spacing: 0.04em;
  line-height: 1.25rem;
  white-space: initial;
}
.chip-tag,
.skeleton-tag .v-skeleton-loader__chip {
  margin: 0.3rem;
  span {
    font-weight: 700;
    margin-right: 0.2rem;
  }
}
</style>
