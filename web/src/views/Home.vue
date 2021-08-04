<template>
  <v-container>
    <v-row>
      <v-col v-if="isConnected" cols="12" md="2" class="hidden-sm-and-down">
        <v-sheet rounded="lg" color="backgroundAlt">
          <admin-actions />
        </v-sheet>
      </v-col>

      <v-col cols="12" md="8">
        <v-sheet min-height="70vh" rounded="lg" color="backgroundAlt">
          <latest-chapters />
        </v-sheet>
      </v-col>

      <v-col cols="12" :md="isConnected ? 2 : 4">
        <v-sheet rounded="lg" min-height="268" color="backgroundAlt">
          <latest-manga />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import AdminActions from "@/components/AdminActions.vue";
import LatestChapters from "@/components/LatestChapters.vue";
import LatestManga from "@/components/LatestManga.vue";

export default Vue.extend({
  name: "Home",

  components: {
    LatestChapters,
    AdminActions,
    LatestManga,
  },
  computed: {
    isConnected: function () {
      return this.$store.getters.isConnected;
    },
  },
});
</script>
