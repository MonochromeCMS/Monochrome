<template>
  <v-row class="ma-0">
    <v-btn block text width="15rem" @click="previousChapter" class="mb-3"> Previous chapter </v-btn>
    <v-col :class="webtoon ? 'webtoon' : ''" cols="12" v-for="index in length" :key="index">
      <v-img
        contain
        :class="fit"
        :width="width"
        :src="`/media/${manga}/${chapter}/${index}.jpg?version=${version}`"
      >
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular indeterminate />
          </v-row>
        </template>
      </v-img>
    </v-col>
    <v-btn block text width="15rem" @click="nextChapter" class="mt-3"> Next chapter </v-btn>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator';

@Component
export default class VerticalReader extends Vue {
  @Prop(String) readonly manga!: string;

  @Prop(String) readonly chapter!: string;

  @Prop(Number) readonly version!: number;

  @Prop(Number) readonly length!: number;

  @Prop(Boolean) readonly webtoon!: boolean;

  @Emit('next')
  nextChapter() {
    return true;
  }

  @Emit('previous')
  previousChapter() {
    return true;
  }

  get fit(): string {
    return this.webtoon ? 'mx-auto' : this.$store.getters.getFit;
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
  height: calc(100vh - 5rem);
  margin: auto;
  max-width: 100%;
}
</style>
