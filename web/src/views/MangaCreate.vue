<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10" md="8" lg="6" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk">
            CREATE MANGA
          </v-card-title>
          <v-card-text>
            <manga-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import MangaForm from "@/components/MangaForm.vue";

@Component({
  components: { MangaForm },
})
export default class MangaCreate extends Vue {
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  mounted(): void {
    if (!this.isConnected) this.$router.replace("/");
  }
}
</script>
