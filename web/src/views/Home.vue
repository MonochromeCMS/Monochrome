<template>
  <v-container>
    <v-row>
      <v-col v-if="isConnected" lg="2" class="hidden-md-and-down">
        <v-sheet rounded="lg" color="backgroundAlt pa-1">
          <admin-actions :left="false" />
        </v-sheet>
      </v-col>

      <v-col cols="12" md="8" :lg="isConnected ? 6 : 8">
        <v-sheet rounded="lg" color="backgroundAlt">
          <latest-chapters />
        </v-sheet>
      </v-col>

      <v-col cols="12" md="4">
        <v-sheet rounded="lg" color="backgroundAlt">
          <latest-manga />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AdminActions from '@/components/AdminActions.vue';
import LatestChapters from '@/components/LatestChapters.vue';
import LatestManga from '@/components/LatestManga.vue';

@Component({
  components: { AdminActions, LatestChapters, LatestManga },
})
export default class Home extends Vue {
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }
}
</script>
