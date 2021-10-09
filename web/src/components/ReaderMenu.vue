<template>
  <v-dialog max-width="30rem" v-model="menu">
    <template v-slot:activator="{ on, attrs }">
      <v-btn fab outlined v-on="on" v-bind="attrs" class="reader-button" color="primary">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </template>
    <v-card rounded="lg" color="backgroundAlt">
      <v-card-title>
        <router-link :to="`/manga/${chapter.manga.id}`" class="text-decoration-none">
          {{ chapter.manga.title }}
        </router-link>
        <v-btn icon class="ml-auto" @click="menu = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-select
          label="Chapter"
          hide-details
          :value="chapter.id"
          :items="chapterItems"
          @change="goToChapter"
        />
        <v-divider class="mt-3" />
        <v-subheader> Reader settings </v-subheader>
        <v-select label="Reader Mode" hide-details v-model="readerMode" :items="modeItems" />
        <!-- Width setting -->
        <v-slider
          class="ma-4 mb-1"
          v-if="readerMode === 'Webtoon'"
          hide-details
          v-model="width"
          step="5"
          min="5"
          thumb-color="text--primary background"
          max="100"
          label="Width"
          thumb-label
        >
          <template v-slot:thumb-label="{ value }"> {{ value }}% </template>
        </v-slider>
        <!-- Fit setting -->
        <v-row v-else align="center" class="ma-1">
          <v-col class="text-body-1"> Image fit: </v-col>
          <v-col class="text-right pa-2">
            <v-btn-toggle v-model="fit" mandatory>
              <v-btn color="background">
                <v-icon>mdi-arrow-expand-horizontal</v-icon>
              </v-btn>
              <v-btn color="background"> Default </v-btn>
              <v-btn color="background">
                <v-icon>mdi-arrow-expand-vertical</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
        <!-- Direction setting -->
        <v-row align="center" class="ma-1" v-if="['Single', 'Double'].includes(readerMode)">
          <v-col class="text-body-1"> Page direction: </v-col>
          <v-col class="text-right pa-2">
            <v-btn-toggle v-model="direction" mandatory>
              <v-btn color="background"><v-icon>mdi-arrow-left</v-icon></v-btn>
              <v-btn color="background"><v-icon>mdi-arrow-right</v-icon></v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
        <!-- Double parity setting -->
        <v-row align="center" class="ma-1" v-if="readerMode === 'Double'">
          <v-col class="text-body-1"> Double page parity: </v-col>
          <v-col class="text-right pa-2">
            <v-btn-toggle v-model="doubleParity" mandatory>
              <v-btn color="background">Even</v-btn>
              <v-btn color="background">Odd</v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator';

@Component
export default class ReaderMenu extends Vue {
  @Prop() readonly chapter!: any;

  @Prop() readonly chapterItems!: any;

  menu = false;

  @Emit()
  goToChapter(id: string): string {
    return id;
  }

  get modeItems(): string[] {
    return this.chapter.webtoon ? ['Webtoon'] : ['Single', 'Double', 'Vertical'];
  }

  get doubleParity(): number {
    return this.$store.getters.getParity;
  }

  set doubleParity(value: number) {
    this.$store.commit('setParity', value);
  }

  get fit(): number {
    const value = this.$store.getters.getFit;
    switch (value) {
      case 'width':
        return 0;
      case 'height':
        return 2;
      default:
        return 1;
    }
  }

  set fit(value: number) {
    switch (value) {
      case 0:
        this.$store.commit('setFit', 'width');
        break;
      case 2:
        this.$store.commit('setFit', 'height');
        break;
      default:
        this.$store.commit('setFit', 'default');
        break;
    }
  }

  get width(): number {
    return Number(this.$store.getters.getWidth.slice(0, -1));
  }

  set width(value: number) {
    this.$store.commit('setWidth', `${value}%`);
  }

  get direction(): number {
    return this.$store.getters.getDirection;
  }

  set direction(value: number) {
    this.$store.commit('setDirection', value);
  }

  get readerMode(): string {
    return this.chapter.webtoon ? 'Webtoon' : this.$store.getters.getReaderMode;
  }

  set readerMode(value: string) {
    if (!this.chapter.webtoon) {
      this.$store.commit('setReaderMode', value);
    }
  }
}
</script>

<style>
.reader-button {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
}
</style>
