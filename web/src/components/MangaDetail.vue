<template>
  <v-container> Manga id: {{ manga }} </v-container>
</template>

<script type="ts">
import Vue from "vue";

export default Vue.extend({
  name: "MangaDetail",
  data: () => ({
    manga: "",
  }),
  mounted() {
    this.manga = this.$route.params.manga;
  }
});
</script>
