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
          <v-col class="mx-auto d-flex align-center" cols="12" sm="10" md="6" lg="5" style="height: calc(100vh - 8rem)">
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
          />
          <v-img
            :class="`${fit} half-page right`"
            contain
            :src="urls[2 * index - 1]"
            :alt="`Page ${2 * index}`"
          />
        </div>
        <v-img
          v-else
          :class="fit"
          contain
          :src="urls[index - 1]"
          :alt="`Page ${index}`"
        />
      </v-carousel-item>
      <v-carousel-item :key="amountTabs + 1">
        <v-row>
          <v-col class="mx-auto d-flex align-center" cols="12" sm="10" md="6" lg="5" style="height: calc(100vh - 8rem)">
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

<script>
import Vue from "vue";

export default Vue.extend({
  name: "PagedReader",
  props: [
    "manga",
    "chapter",
    "version",
    "length",
    "double",
  ],
  data: () => ({
    currentPage: null,
    test: null,
  }),
  methods: {
    handleArrows(ev) {
      switch (ev.code) {
        case "KeyA":
        case "ArrowLeft":
          this.currentPage -= 1;
          break;
        case "KeyD":
        case "ArrowRight":
          this.currentPage += 1;
      }
    },
  },
  computed: {
    fit() {
      return this.$store.getters.getFit;
    },
    reverse() {
      return !this.$store.getters.getDirection;
    },
    parity() {
      return this.$store.getters.getParity;
    },
    amountTabs() {
      return this.double
        ? Math.ceil((this.length + this.parity) / 2)
        : this.length;
    },
    urls() {
      let result = Array.from(
        { length: this.length },
        (_, i) =>
          `/media/${this.manga}/${this.chapter}/${i + 1}.jpg?version=${
            this.version
          }`
      );

      if (this.double) {
        if (this.parity) {
          result = [null].concat(result);
        }
        if (result.length % 2 !== 0) {
          result.push(null);
        }
      }

      return this.reverse ? result.reverse() : result;
    },
  },
  watch: {
    chapter() {
      this.currentPage = this.reverse ? this.amountTabs : 1;
    },
    reverse() {
      this.currentPage = this.amountTabs - this.currentPage + 1;
    },
    parity(value) {
      switch (true) {
        case this.double && value && this.length % 2 === 0:
          this.currentPage += this.reverse;
          break;
        case this.double && this.length % 2 === 0:
          this.currentPage -= this.reverse;
      }
    },
    currentPage(value) {
      switch (true) {
        case value === this.amountTabs + 1 && !this.reverse:
        case value === 0 && this.reverse:
          this.$emit("next", 1);
          break;
        case value === this.amountTabs + 1 && this.reverse:
        case value === 0 && !this.reverse:
          this.$emit("previous", 1);
      }
    },
    double(value) {
      if (value) {
        this.currentPage = Math.ceil((this.currentPage + this.reverse) / 2);
      } else {
        this.currentPage = this.currentPage * 2 - 1;
      }
    },
  },
  mounted() {
    this.currentPage = this.reverse ? this.amountTabs : 1;
    document.addEventListener("keyup", this.handleArrows);
  },
});
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
  max-height: calc(100vh - 10rem);
  max-width: 100%;
  &.half-page {
    max-width: 50%;
  }
}
.reader-tabs {
  position: sticky;
  top: 3.7rem;
  z-index: 1;
  border-radius: 0.3rem;
  margin-bottom: .8rem;
}
</style>
