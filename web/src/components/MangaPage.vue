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
          <v-responsive aspect-ratio="1">
            <v-skeleton-loader type="image" class="skeleton-image fill-height" />
          </v-responsive>
          <v-skeleton-loader type="article, divider" />
          <v-skeleton-loader type="chip" class="skeleton-chip" />
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col v-if="manga.length === 0" class="text-center text-body-1">
        {{ search ? 'No manga could be found.' : 'No manga has been added yet.' }}
      </v-col>
      <v-col v-else cols="12" sm="6" md="4" lg="3" v-for="(item, index) in manga" :key="index">
        <v-card color="background" :to="to(item)" height="100%" class="d-flex flex-column">
          <v-img aspect-ratio="1" :src="cover(item)"></v-img>
          <v-card-title v-text="item.title" />
          <v-card-subtitle v-text="item.author" />
          <v-card-text v-text="item.description" class="card-description"></v-card-text>
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
        color="background text--primary"
        v-model="page"
        :length="pageAmount"
      ></v-pagination>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import SearchBar from '@/components/SearchBar.vue';
import type { MangaResponse } from '@/api/Manga';
import Manga from '@/api/Manga';

@Component({
  components: { SearchBar },
})
export default class MangaPage extends Vue {
  loading = true;

  manga: MangaResponse[] = [];

  limit = 12;

  page = 1;

  total = 0;

  statusColor = {
    ongoing: 'green',
    completed: 'green darken-2',
    hiatus: 'orange',
    cancelled: 'red',
  };

  search: any = '';

  get offset(): number {
    return (this.page - 1) * this.limit;
  }

  get pageAmount(): number {
    return Math.ceil(this.total / this.limit);
  }

  cover(manga: MangaResponse): string {
    return `/media/${manga.id}/cover.jpg?version=${manga.version}`;
  }

  to(manga: MangaResponse): string {
    return `/manga/${manga.id}`;
  }

  async getManga(): Promise<void> {
    const response = await Manga.search(this.search, this.limit, this.offset, this.loading);

    if (response.data) {
      this.manga = response.data.results;
      this.total = response.data.total;
    } else {
      const notification = {
        context: 'Manga pagination',
        message: response.error ?? '',
        color: 'error',
      };
      this.$store.commit('addNotification', notification);
    }

    this.loading = false;
  }

  upper(status: string): string {
    return status ? status.charAt(0).toUpperCase() + status.slice(1) : '';
  }

  @Watch('page')
  onPageUpdate(): void {
    this.getManga();
  }

  @Watch('search')
  onSearch(): void {
    if (this.page === 1) {
      this.getManga();
    } else {
      this.page = 1;
    }
  }

  mounted(): void {
    if (this.$route.query.q) {
      this.search = this.$route.query.q.length ? this.$route.query.q[0] : this.$route.query.q;
    } else {
      this.getManga();
    }
  }
}
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

.skeleton-image .v-skeleton-loader__image {
  height: 100%;
}
</style>
