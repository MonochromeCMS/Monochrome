<template>
  <v-row class="ma-0">
    <v-col
      :class="webtoon ? 'webtoon' : ''"
      v-for="index in length"
      :key="index"
    >
      <v-img
        contain
        :class="fit"
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
    return this.$store.getters.getFit;
  }
}
</script>

<style lang="scss">
.webtoon {
  padding: 0;
}
.default {
  max-height: 150vh;
  max-width: 100%;
}
.width {
  width: 100%;
}
.height {
  max-height: calc(100vh - 10rem);
  max-width: 100%;
}
</style>
