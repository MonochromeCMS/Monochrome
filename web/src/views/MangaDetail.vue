<template>
  <v-container>
    <v-row>
      <v-col>
        <v-sheet rounded="lg" color="backgroundAlt" min-height="30vh">
          <manga-detail />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script type="ts">
import Vue from "vue";
import MangaDetail from "@/components/MangaDetail.vue";

export default Vue.extend({
  components: {MangaDetail}
});
</script>
