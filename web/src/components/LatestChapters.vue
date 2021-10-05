<template>
  <v-container>
    <v-card-title class="justify-center lemon-milk"> Latest chapters </v-card-title>
    <v-row v-if="loading" class="mx-0 mb-0">
      <v-col
        cols="12"
        sm="6"
        :lg="isConnected ? 12 : 6"
        xl="6"
        v-for="index in limit"
        :key="index"
        class="px-2 my-2"
      >
        <v-card color="background" class="px-4">
          <v-row align="center">
            <v-col cols="3">
              <v-responsive max-height="7rem">
                <v-skeleton-loader type="image" />
              </v-responsive>
            </v-col>
            <v-col cols="8" class="d-flex flex-column justify-center">
              <h2>
                <v-skeleton-loader type="text" />
              </h2>
              <h3>
                <v-skeleton-loader type="text" />
              </h3>
              <h4>
                <v-skeleton-loader type="text" />
              </h4>
              <v-skeleton-loader type="chip" />
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else class="mx-0 mb-0">
      <v-col cols="12" class="text-center text-body-1" v-if="chapters.length === 0">
        No chapters have been uploaded yet.
      </v-col>
      <v-col
        cols="12"
        sm="6"
        :lg="isConnected ? 12 : 6"
        xl="6"
        v-for="(chapter, index) in chapters"
        :key="index"
        class="px-2 my-2"
      >
        <v-card color="background" class="px-4" :to="`/chapters/${chapter.id}`">
          <v-row align="center">
            <v-col cols="3">
              <v-img
                :src="`/media/${chapter.mangaId}/cover.jpg?version=${chapter.manga.version}`"
                max-height="7rem"
              />
            </v-col>
            <v-col cols="8" class="d-flex flex-column justify-center">
              <h2 class="text-subtitle-1 ellipsis">
                {{ chapter.manga.title }}
              </h2>
              <h3 class="text-subtitle-2 ellipsis">
                {{ `Chapter ${chapter.number}${chapter.name ? ' - ' + chapter.name : ''}` }}
              </h3>
              <h4 class="text-caption">{{ chapter.scanGroup }}</h4>
              <v-chip color="backgroundAlt" class="chip-tag">
                {{ ago(new Date(chapter.uploadTime).getTime()) }} ago
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
        color="background text--primary"
        v-model="page"
        :length="pageAmount"
      >
      </v-pagination>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import type { DetailedChapterResponse } from '@/api/Chapter';
import Chapter from '@/api/Chapter';

@Component
export default class LatestChapters extends Vue {
  page = 1;

  limit = 8;

  total = 0;

  loading = true;

  chapters: DetailedChapterResponse[] = [];

  get pageAmount(): number {
    return Math.ceil(this.total / this.limit);
  }

  get offset(): number {
    return (this.page - 1) * this.limit;
  }

  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  @Watch('page')
  async onPageChange(): Promise<void> {
    await this.getChapters();
  }

  async getChapters(): Promise<void> {
    const response = await Chapter.latest(this.limit, this.offset, this.loading);

    if (response.data) {
      this.chapters = response.data.results;
      this.total = response.data.total;
    } else {
      const notification = {
        context: 'Latest chapters',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }

    this.loading = false;
  }

  ago(val: number): string {
    val = 0 | ((Date.now() - val) / 1000);
    const length: Record<string, number> = {
      second: 60,
      minute: 60,
      hour: 24,
      day: 7,
      week: 4.35,
      month: 12,
      year: 10000,
    };

    for (const unit of Object.keys(length)) {
      const result = val % length[unit];
      if (!(val = 0 | (val / length[unit]))) return result + ' ' + (result - 1 ? unit + 's' : unit);
    }
    return 'ERROR';
  }

  mounted(): void {
    this.getChapters();
  }
}
</script>

<style lang="scss">
.v-chip.chip-tag {
  margin-top: 0.2rem;
  max-width: max-content;
}
.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
