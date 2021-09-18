<template>
  <div style="position: relative">
    <v-tabs
      v-model="currentPage"
      background-color="backgroundAlt"
      show-arrows
      centered
      center-active
      class="reader-tabs"
    >
      <v-tab :key="0">
        {{ reverse ? "Next chapter" : "Previous chapter" }}
      </v-tab>
      <v-tab v-for="index in amountTabs" :key="index">
        {{ reverse ? amountTabs - index + 1 : index }}
      </v-tab>
      <v-tab :key="amountTabs + 1">
        {{ reverse ? "Previous chapter" : "Next chapter" }}
      </v-tab>
    </v-tabs>

    <v-carousel
      height="auto"
      hide-delimiters
      v-model="currentPage"
      :continuous="false"
    >
      <v-carousel-item :key="0">
        <v-row>
          <v-col
            class="mx-auto d-flex align-center"
            cols="12"
            sm="10"
            md="6"
            lg="5"
            style="height: calc(100vh - 8rem)"
          >
            <v-sheet rounded="lg">
              <v-row
                class="fill-height text-center ma-0 pa-10"
                align="center"
                justify="center"
              >
                <div class="text-h2">
                  {{
                    reverse
                      ? "This is the latest chapter available, thanks for reading!"
                      : "This is the first chapter"
                  }}
                </div>
              </v-row>
            </v-sheet>
          </v-col>
        </v-row>
      </v-carousel-item>
      <v-carousel-item v-for="index in amountTabs" :key="index">
        <div v-if="double" class="d-flex justify-center">
          <v-img
            :class="`${fit} half-page left`"
            contain
            :src="urls[2 * index - 2]"
            :alt="`Page ${2 * index - 1}`"
          >
            <template v-slot:placeholder>
              <v-row
                class="fill-height ma-0"
                align="center"
                justify="center"
              >
                <v-progress-circular indeterminate />
              </v-row>
            </template>
          </v-img>
          <v-img
            :class="`${fit} half-page right`"
            contain
            :src="urls[2 * index - 1]"
            :alt="`Page ${2 * index}`"
          >
            <template v-slot:placeholder>
              <v-row
                class="fill-height ma-0"
                align="center"
                justify="center"
              >
                <v-progress-circular indeterminate />
              </v-row>
            </template>
          </v-img>
        </div>
        <v-img
          v-else
          :class="fit"
          contain
          :src="urls[index - 1]"
          :alt="`Page ${index}`"
        >
          <template v-slot:placeholder>
            <v-row
              class="fill-height ma-0"
              align="center"
              justify="center"
            >
              <v-progress-circular indeterminate />
            </v-row>
          </template>
        </v-img>
      </v-carousel-item>
      <v-carousel-item :key="amountTabs + 1">
        <v-row>
          <v-col
            class="mx-auto d-flex align-center"
            cols="12"
            sm="10"
            md="6"
            lg="5"
            style="height: calc(100vh - 8rem)"
          >
            <v-sheet rounded="lg">
              <v-row
                class="fill-height text-center ma-0 pa-10"
                align="center"
                justify="center"
              >
                <div class="text-h2">
                  {{
                    reverse
                      ? "This is the first chapter"
                      : "This is the latest chapter available, thanks for reading!"
                  }}
                </div>
              </v-row>
            </v-sheet>
          </v-col>
        </v-row>
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from "vue-property-decorator";

@Component
export default class PagedReader extends Vue {
  @Prop(String) readonly manga!: string;
  @Prop(String) readonly chapter!: string;
  @Prop(Number) readonly version!: number;
  @Prop(Number) readonly length!: number;
  @Prop(Boolean) readonly double!: boolean;

  currentPage: number | null = null;

  handleArrows(ev: KeyboardEvent): void {
    if (this.currentPage === null) {
      return;
    }

    switch (ev.code) {
      case "KeyA":
      case "ArrowLeft":
        this.currentPage -= 1;
        break;
      case "KeyD":
      case "ArrowRight":
        this.currentPage += 1;
    }
  }

  get fit(): string {
    return this.$store.getters.getFit;
  }

  get reverse(): boolean {
    return !this.$store.getters.getDirection;
  }

  get parity(): number {
    return this.$store.getters.getParity;
  }

  get amountTabs(): number {
    return this.double
      ? Math.ceil((this.length + this.parity) / 2)
      : this.length;
  }

  get urls(): (string | null)[] {
    let result: (string | null)[] = Array.from(
      { length: this.length },
      (_, i) =>
        `/media/${this.manga}/${this.chapter}/${i + 1}.jpg?version=${
          this.version
        }`
    );

    if (this.double) {
      if (this.parity) {
        const tempResult: (string | null)[] = [null];
        result = tempResult.concat(result);
      }
      if (result.length % 2 !== 0) {
        result.push(null);
      }
    }

    return this.reverse ? result.reverse() : result;
  }

  @Watch("chapter")
  onChapterChange(): void {
    this.currentPage = this.reverse ? this.amountTabs : 1;
  }

  @Watch("reverse")
  onDirectionChange(): void {
    if (this.currentPage == null) {
      return;
    }

    this.currentPage = this.amountTabs - this.currentPage + 1;
  }

  @Watch("parity")
  onParityChange(value: boolean): void {
    if (this.currentPage == null) {
      return;
    }

    switch (true) {
      case this.double && value && this.length % 2 === 0:
        this.currentPage += Number(this.reverse);
        break;
      case this.double && this.length % 2 === 0:
        this.currentPage -= Number(this.reverse);
    }
  }

  @Watch("currentPage")
  onPageChange(value: number): void {
    switch (true) {
      case value === this.amountTabs + 1 && !this.reverse:
      case value === 0 && this.reverse:
        this.$emit("next", 1);
        break;
      case value === this.amountTabs + 1 && this.reverse:
      case value === 0 && !this.reverse:
        this.$emit("previous", 1);
    }
  }

  @Watch("double")
  onDoubleChange(value: boolean): void {
    if (this.currentPage == null) {
      return;
    }

    if (value) {
      this.currentPage = Math.ceil(
        (this.currentPage + Number(this.reverse)) / 2
      );
    } else {
      this.currentPage = this.currentPage * 2 - 1;
    }
  }

  mounted(): void {
    this.currentPage = this.reverse ? this.amountTabs : 1;
    document.addEventListener("keyup", this.handleArrows);
  }
}
</script>

<style lang="scss">
.half-page {
  &.left .v-image__image {
    background-position: right center !important;
  }
  &.right .v-image__image {
    background-position: left center !important;
  }
}
.default {
  max-height: 150vh;
  max-width: 100%;
  &.half-page {
    max-width: 50%;
  }
}
.width {
  width: 100%;
  &.half-page {
    width: 50%;
  }
}
.height {
  max-height: calc(100vh - 5rem);
  max-width: 100%;
  &.half-page {
    max-width: 50%;
  }
}
.reader-tabs {
  position: sticky;
  top: .7rem;
  z-index: 1;
  border-radius: 0.3rem;
  margin-bottom: 0.8rem;
}
</style>
