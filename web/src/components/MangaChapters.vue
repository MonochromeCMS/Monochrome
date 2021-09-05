<template>
  <v-container>
    <v-row v-if="loading" class="flex-column align-center">
      <v-col cols="12" class="text-h3 text-center" tag="h2"> Chapters </v-col>
      <v-col v-for="i in limit" :key="i">
        <v-row class="justify-space-around background">
          <v-col cols="7" sm="4" md="3">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-col cols="3" md="4" class="hidden-sm-and-down">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-col cols="5" sm="3" md="2">
            <v-skeleton-loader type="heading" />
          </v-col>
          <v-col cols="3" lg="2" class="pa-0 text-right hidden-xs-only">
            <v-skeleton-loader type="chip" class="ma-2" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-else class="flex-column align-center">
      <v-col cols="12" class="text-h3 text-center" tag="h2"> Chapters </v-col>
      <v-col
        cols="12"
        v-for="(item, index) in chaptersPage"
        :key="index"
        class="chapter-row pa-1"
      >
        <router-link
          :to="`/chapters/${item.id}`"
          class="text-decoration-none chapter-link pa-3"
        >
          <v-row class="justify-space-around">
            <v-col cols="7" sm="4" md="3">
              {{ item.volume ? `Vol ${item.volume} ` : "" }}Chapter
              {{ item.number }}
            </v-col>
            <v-col cols="3" md="4" class="hidden-sm-and-down ellipsis">
              {{ item.name }}
            </v-col>
            <v-col cols="5" sm="3" md="2" class="ellipsis">
              {{ item.scanGroup }}
            </v-col>
            <v-col cols="3" lg="2" class="pa-0 text-right hidden-xs-only">
              <v-chip color="backgroundAlt" class="ma-2">
                {{ ago(new Date(item.uploadTime).getTime()) }} ago
              </v-chip>
            </v-col>
          </v-row>
        </router-link>
        <v-menu v-if="isConnected" offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-on="on"
              v-bind="attrs"
              class="mr-1"
              aria-label="More options"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-btn block color="background" :to="`/chapters/${item.id}/edit`">
            Edit chapter
          </v-btn>
          <chapter-delete :id="item.id" @input="popChapter(index)" />
        </v-menu>
      </v-col>
      <v-col
        cols="12"
        class="text-body-1 text-center"
        v-if="chapters.length === 0"
      >
        No chapters have been uploaded yet.
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
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import ChapterDelete from "@/components/ChapterDelete.vue";
import type { ChapterResponse } from "@/api/Chapter";
import Manga from "@/api/Manga";

@Component({
  components: { ChapterDelete },
})
export default class MangaChapters extends Vue {
  @Prop() readonly value!: string;
  @Prop() readonly mangaId!: string;

  chapters: ChapterResponse[] = [];
  loading = true;
  limit = 10;
  page = 1;
  innerValue = ["", ""];

  get pageAmount(): number {
    return Math.ceil(this.chapters.length / this.limit);
  }
  get chaptersPage(): any[] {
    const start = this.limit * (this.page - 1);
    return this.chapters.slice(start, start + this.limit);
  }
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  popChapter(index: number): void {
    this.chapters.splice(index, 1);
  }

  dispatchValue(
    error: string | null = null,
    chapter: string | null = null
  ): void {
    const value = [error || this.innerValue[0], chapter || this.innerValue[1]];
    this.innerValue = value;
    this.$emit("input", value);
    this.$emit("update:value", value);
  }

  async getChapters(): Promise<void> {
    const response = await Manga.chapters(this.mangaId, this.loading);

    if (response.data) {
      this.chapters = response.data;
    } else {
      this.dispatchValue(response.error ?? "");
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
      if (!(val = 0 | (val / length[unit])))
        return result + " " + (result - 1 ? unit + "s" : unit);
    }
    return "ERROR";
  }

  @Watch("chapters")
  onChaptersUpdate(): void {
    if (this.chapters.length > 0) {
      this.dispatchValue(null, this.chapters[this.chapters.length - 1]?.id);
    }
  }

  mounted(): void {
    this.getChapters();
  }
}
</script>

<style lang="scss">
.chapter-row {
  display: flex;
  align-items: center;
  .chapter-link {
    width: 100%;
    height: 100%;
  }
}
.theme--dark {
  .chapter-row {
    background-color: black;
    &:hover {
      background-color: #424242;
    }
    border-bottom: #212121 0.1rem solid;
    &:last-child {
      border-bottom: none;
    }
  }
}
.theme--light {
  .chapter-row {
    background-color: #eeeeee;
    &:hover {
      background-color: #e0e0e0;
    }
    border-bottom: #ffffff 0.1rem solid;
    &:last-child {
      border-bottom: none;
    }
  }
}
.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
