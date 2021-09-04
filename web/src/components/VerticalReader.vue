<template>
  <v-row class="ma-0">
    <v-col
      :class="webtoon ? 'webtoon' : ''"
      cols="12"
      v-for="index in length"
      :key="index"
    >
      <v-img
        contain
        :class="fit"
        :width="width"
        :src="`/media/${manga}/${chapter}/${index}.jpg?version=${version}`"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component
export default class VerticalReader extends Vue {
  @Prop(String) readonly manga!: string;
  @Prop(String) readonly chapter!: string;
  @Prop(Number) readonly version!: number;
  @Prop(Number) readonly length!: number;
  @Prop(Boolean) readonly webtoon!: boolean;

  get fit(): string {
    return this.webtoon ? "mx-auto" : this.$store.getters.getFit;
  }

  get width(): string {
    return !this.webtoon ? null : this.$store.getters.getWidth;
  }
}
</script>

<style lang="scss">
.webtoon {
  padding: 0;
}
.default {
  margin: auto;
  max-height: 150vh;
  max-width: 100%;
}
.width {
  width: 100%;
}
.height {
  max-height: calc(100vh - 8rem);
  margin: auto;
  max-width: 100%;
}
</style>
