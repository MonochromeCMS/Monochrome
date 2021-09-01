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
      <validation-provider
        v-slot="{ errors }"
        name="Cover"
        :rules="this.manga ? '' : 'required'"
      >
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
          {{ this.manga ? "Edit Manga" : "Create Manga" }}
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";
import { required, digits } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import axios, { AxiosRequestConfig } from "axios";
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

@Component({
  components: {
    MangaRow,
    ValidationProvider,
    ValidationObserver,
  },
})
export default class MangaForm extends Vue {
  @Prop() readonly manga!: Record<string, any>;

  title = "";
  description = "";
  author = "";
  artist = "";
  year = null;
  status = null;
  alert = "";
  cover = null;
  buffer = null;
  statusItems = [
    { value: "ongoing", text: "Ongoing" },
    { value: "hiatus", text: "Hiatus" },
    { value: "completed", text: "Completed" },
    { value: "cancelled", text: "Cancelled" },
  ];

  get params(): any {
    return {
      title: this.title,
      description: this.description,
      author: this.author,
      artist: this.artist,
      year: this.year || null,
      status: this.status,
    };
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  url(blob: File | null): string | null {
    if (blob) {
      return blob ? URL.createObjectURL(blob) : null;
    } else {
      return this.manga
        ? `/media/${this.manga.id}/cover.jpg?version=${this.manga.version}`
        : null;
    }
  }

  async submit(): Promise<void> {
    //@ts-ignore I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      if (this.manga) {
        await this.editManga(this.params, this.manga.id);
      } else {
        await this.createManga(this.params);
      }
    }
  }

  clear(): void {
    this.alert = "";
    this.title = "";
    this.description = "";
    this.author = "";
    this.artist = "";
    this.year = null;
    this.status = null;
  }

  async createManga(params: any): Promise<void> {
    const config = this.authConfig;
    config.headers["Content-Type"] = "application/json";

    let response;
    try {
      response = await axios.post("/api/manga", params, config);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 201:
        await this.setCover(response.data.id, this.cover);
        break;
      case 401:
        this.$store.commit("logout");
        break;
      default:
        this.alert = response.data.detail ?? response.statusText;
    }
  }

  async editManga(params: any, id: string): Promise<void> {
    const config = this.authConfig;
    config.headers["Content-Type"] = "application/json";

    let response;
    try {
      response = await axios.put(`/api/manga/${id}`, params, config);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 200:
        if (this.cover) {
          await this.setCover(id, this.cover);
        } else {
          await this.$router.push(`/manga/${id}`);
        }
        break;
      case 401:
        this.$store.commit("logout");
        break;
      default:
        this.alert = response.data.detail ?? response.statusText;
    }
  }

  async setCover(mangaId: string, cover: File | null): Promise<void> {
    if (!cover) return;

    const config = this.authConfig;
    config.headers["Content-Type"] = "multipart/form-data";

    const form = new FormData();
    form.append("payload", cover);

    let response;
    try {
      response = await axios.put(`/api/manga/${mangaId}/cover`, form, config);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 200:
        await this.$router.push(`/manga/${mangaId}`);
        break;
      case 401:
        this.$store.commit("logout");
        break;
      default:
        this.alert = response.data.detail ?? response.statusText;
    }
  }

  mounted(): void {
    if (this.manga) {
      this.title = this.manga.title;
      this.description = this.manga.description;
      this.author = this.manga.author;
      this.artist = this.manga.artist;
      this.year = this.manga.year;
      this.status = this.manga.status;
    }
  }
}
</script>
