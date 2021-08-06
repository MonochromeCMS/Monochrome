<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10" md="8" lg="6" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk"
            >CREATE MANGA</v-card-title
          >
          <v-card-text>
            <manga-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script type="ts">
import Vue from "vue";
import MangaForm from "@/components/MangaForm.vue";

export default Vue.extend({
  components: {MangaForm}
});
</script>
