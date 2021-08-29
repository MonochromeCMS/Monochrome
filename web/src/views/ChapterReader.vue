<template>
  <v-container fluid class="reader">
    <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
    <v-row v-if="chapter">
      <v-col cols="12" v-if="['Vertical', 'Webtoon'].includes(readerMode)">
        <vertical-reader
          :manga="chapter.manga.id"
          :chapter="chapter.id"
          :version="chapter.version"
          :length="chapter.length"
          :webtoon="readerMode === 'Webtoon'"
        />
      </v-col>
      <v-col cols="12" v-if="['Single', 'Double'].includes(readerMode)">
        <paged-reader
          :manga="chapter.manga.id"
          :chapter="chapter.id"
          :version="chapter.version"
          :length="chapter.length"
          :double="readerMode === 'Double'"
          @next="goToChapter(nextChapter)"
          @previous="goToChapter(previousChapter)"
        />
      </v-col>
    </v-row>
    <reader-menu
      v-if="chapter"
      :chapter="chapter"
      :chapter-items="chapterItems"
      @go-to-chapter="goToChapter"
    />
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import axios from "axios";
import PagedReader from "@/components/PagedReader.vue";
import VerticalReader from "@/components/VerticalReader.vue";
import ReaderMenu from "@/components/ReaderMenu.vue";

@Component({
  components: { ReaderMenu, VerticalReader, PagedReader },
})
export default class ChapterReader extends Vue {
  chapter = null;
  chapters: any[] = [];
  alert = "";

  get chapterId(): string {
    return this.$route.params.chapter;
  }

  get currentChapterIndex(): number {
    return this.chapters.findIndex((el) => el.id === this.chapterId);
  }

  get previousChapter(): string | null {
    if (
      this.currentChapterIndex !== -1 &&
      this.currentChapterIndex < this.chapters.length - 1
    ) {
      return this.chapters[this.currentChapterIndex + 1].id;
    } else {
      return null;
    }
  }

  get nextChapter(): string | null {
    if (this.currentChapterIndex > 0) {
      return this.chapters[this.currentChapterIndex - 1].id;
    } else {
      return null;
    }
  }

  get chapterItems(): any[] {
    return this.chapters.map((el) => ({
      value: el.id,
      text: this.chapterName(el),
    }));
  }

  get readerMode(): string {
    return this.$store.getters.getReaderMode;
  }

  async goToChapter(id: string | null): Promise<void> {
    if (id) {
      await this.$router.push(`/chapters/${id}`);
      await this.getChapter();
    }
  }

  chapterName(chapter: any): string {
    const volume = chapter.volume ? `Vol ${chapter.volume} ` : "";
    const name = chapter.name ? ` - ${chapter.name}` : "";
    return volume + `Ch ${chapter.number}` + name;
  }

  async getChapter(): Promise<void> {
    let url = `/api/chapter/${this.chapterId}`;

    let response;
    try {
      response = await axios.get(url);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 200:
        this.chapter = response.data;
        this.chapters = [
          { value: this.chapterId, text: this.chapterName(response.data) },
        ];
        await this.getChapters(response.data.mangaId);
        break;
      case 404:
        this.alert = "Chapter not found";
        break;
      case 422:
        this.alert = "The ID provided isn't an UUID";
        break;
      default:
        this.alert = response.data?.detail ?? response.statusText;
    }
  }

  async getChapters(mangaId: string): Promise<void> {
    let url = `/api/manga/${mangaId}/chapters`;

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
  }

  mounted(): void {
    this.getChapter();
  }
}
</script>
