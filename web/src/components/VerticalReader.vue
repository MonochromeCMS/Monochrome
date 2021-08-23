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

<script>
import Vue from "vue";

export default Vue.extend({
  name: "VerticalReader",
  props: ["manga", "chapter", "version", "length", "webtoon"],
  computed: {
    fit() {
      return this.$store.getters.getFit;
    },
  },
});
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
