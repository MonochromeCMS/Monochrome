<template>
  <v-dialog v-model="dialog" max-width="30rem">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="error" block v-bind="attrs" v-on="on">
        Delete Chapter
      </v-btn>
    </template>

    <v-card>
      <v-alert type="error" v-if="alert !== ''">{{ alert }}</v-alert>
      <v-card-title class="text-h5 background mb-2"> Warning </v-card-title>

      <v-card-text class="body-1">
        <span class="font-weight-bold">This action can't be undone!</span>
        Are you sure you want to delete this chapter?
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray" text @click="dialog = false"> Cancel </v-btn>
        <v-btn color="error" @click="deleteChapter"> Delete </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Vue from "vue";
import axios from "axios";

export default Vue.extend({
  name: "ChapterDelete",
  props: ["id"],
  data: () => ({
    dialog: false,
    alert: "",
  }),
  computed: {
    authConfig() {
      return this.$store.getters.authConfig;
    },
  },
  methods: {
    async deleteChapter() {
      const config = this.authConfig;

      let url = `/api/chapter/${this.id}`;

      let response;
      try {
        response = await axios.delete(url, config);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
        case 404:
          this.$emit("input", true);
          this.dialog = false;
          break;
        case 401:
          this.$store.commit("logout");
          break;
        case 422:
          this.alert = "The ID provided isn't an UUID";
          break;
        default:
          this.alert = response.statusText;
      }
    },
  },
});
</script>

<style scoped></style>
