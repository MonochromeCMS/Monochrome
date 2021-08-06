<template>
  <validation-observer ref="observer">
    <v-alert type="error" v-if="alert !== ''" dense class="mb-7">
      {{ alert }}
    </v-alert>
    <v-form @submit.prevent="submit">
      <!-- TITLE FIELD -->
      <validation-provider v-slot="{ errors }" name="Title" rules="required">
        <v-text-field
          v-model="title"
          :error-messages="errors"
          label="Title"
          required
          outlined
        ></v-text-field>
      </validation-provider>
      <!-- DESC FIELD -->
      <validation-provider
        v-slot="{ errors }"
        name="Description"
        rules="required"
      >
        <v-textarea
          v-model="description"
          :error-messages="errors"
          label="Description"
          required
          outlined
        ></v-textarea>
      </validation-provider>
      <!-- AUTHOR FIELD -->
      <validation-provider v-slot="{ errors }" name="Author" rules="required">
        <v-text-field
          v-model="author"
          :error-messages="errors"
          label="Author"
          required
          outlined
        ></v-text-field>
      </validation-provider>
      <!-- ARTIST FIELD -->
      <validation-provider v-slot="{ errors }" name="Artist" rules="required">
        <v-text-field
          v-model="artist"
          :error-messages="errors"
          label="Artist"
          required
          outlined
        ></v-text-field>
      </validation-provider>
      <!-- YEAR FIELD -->
      <validation-provider
        v-slot="{ errors }"
        name="Year of release"
        :rules="{
          digits: 4,
        }"
      >
        <v-text-field
          v-model="year"
          :error-messages="errors"
          label="Year of release"
          required
          outlined
        ></v-text-field>
      </validation-provider>
      <!-- STATUS FIELD -->
      <validation-provider v-slot="{ errors }" name="Status" rules="required">
        <v-select
          :items="statusItems"
          v-model="status"
          :error-messages="errors"
          label="Status"
          outlined
        ></v-select>
      </validation-provider>
      <!-- COVER FIELD -->
      <validation-provider v-slot="{ errors }" name="Cover" rules="required">
        <v-file-input
          v-model="cover"
          :error-messages="errors"
          accept="image/*"
          label="Cover"
        >
        </v-file-input>
      </validation-provider>
      <!-- PREVIEW -->
      <v-expansion-panels class="mb-4">
        <v-expansion-panel>
          <v-expansion-panel-header> Preview </v-expansion-panel-header>
          <v-expansion-panel-content>
            <manga-row :loading="false" :manga="params" :cover="url(cover)" />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
      <div class="text-center">
        <v-btn type="submit" block color="background" class="text--primary">
          Create Manga
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { required, digits } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import Vue from "vue";
import axios from "axios";
import MangaRow from "@/components/MangaRow.vue";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});
extend("digits", {
  ...digits,
  message: "{_field_} requires {length} digits ",
});

export default Vue.extend({
  name: "MangaForm",
  components: {
    MangaRow,
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    title: "",
    description: "",
    author: "",
    artist: "",
    year: null,
    status: null,
    alert: "",
    cover: null,
    buffer: null,
    statusItems: [
      { value: "ongoing", text: "Ongoing" },
      { value: "hiatus", text: "Hiatus" },
      { value: "completed", text: "Completed" },
      { value: "cancelled", text: "Cancelled" },
    ],
  }),
  computed: {
    params() {
      return {
        title: this.title,
        description: this.description,
        author: this.author,
        artist: this.artist,
        year: this.year || null,
        status: this.status,
      };
    },
    authStr() {
      return this.$store.getters.authStr;
    },
  },
  methods: {
    url(blob) {
      return blob ? URL.createObjectURL(blob) : null;
    },
    async submit(): Promise<void> {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        await this.createManga(this.params);
      }
    },
    clear(): void {
      this.alert = "";
      this.username = "";
      this.password = "";
      this.$refs.observer.reset();
    },
    async createManga(params): Promise<void> {
      const config = {
        headers: {
          Accept: "*/*",
          Authorization: this.authStr,
          "Content-Type": "application/json",
        },
        withCredentials: true,
      };

      let response;
      try {
        response = await axios.post("/api/manga", params, config);
      } catch (e) {
        response = e.response;
      }

      //TODO: Check the status, show error if needed
      switch (response.status) {
        case 201:
          await this.setCover(response.data.id);
          break;
        case 401:
          this.$store.commit("logout");
          break;
        default:
          this.alert = response.statusText;
      }
    },
    async setCover(manga_id) {
      if (!this.cover) return;

      const config = {
        headers: {
          Accept: "*/*",
          Authorization: this.authStr,
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      };

      const form = new FormData();
      form.append("payload", this.cover);

      let response;
      try {
        response = await axios.put(
          `/api/manga/${manga_id}/cover`,
          form,
          config
        );
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
          await this.$router.push(`/manga/${manga_id}`);
          break;
        case 401:
          this.$store.commit("logout");
          break;
        default:
          this.alert = response.statusText;
      }
    },
  },
});
</script>
