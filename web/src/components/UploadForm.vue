<template>
  <validation-observer ref="observer">
    <v-alert type="error" v-if="alert !== ''" dense class="mb-7">
      {{ alert }}
    </v-alert>
    <v-form @submit.prevent="submit">
      <v-row class="mb-3">
        <!-- VOLUME FIELD -->
        <v-col cols="12" sm="6" md="4" class="pa-3 pb-0">
          <validation-provider
            v-slot="{ errors }"
            name="Volume Number"
            rules="numeric"
          >
            <v-text-field
              v-model="volume"
              :error-messages="errors"
              label="Volume Number"
              required
              hide-details="auto"
              outlined
            ></v-text-field>
          </validation-provider>
        </v-col>
        <!-- NUMBER FIELD -->
        <v-col cols="12" sm="6" md="4" class="pa-3 pb-0">
          <validation-provider
            v-slot="{ errors }"
            name="Chapter Number"
            :rules="{ required: true, regex: /^[0-9.]+$/ }"
          >
            <v-text-field
              v-model="number"
              :error-messages="errors"
              label="Chapter Number"
              required
              hide-details="auto"
              outlined
            ></v-text-field>
          </validation-provider>
        </v-col>
        <!-- GROUP FIELD -->
        <v-col cols="12" md="4" class="pa-3 pb-0">
          <validation-provider
            v-slot="{ errors }"
            name="Scan Group"
            rules="required"
          >
            <v-text-field
              v-model="scan_group"
              :error-messages="errors"
              label="Scan Group"
              required
              hide-details="auto"
              outlined
            ></v-text-field>
          </validation-provider>
        </v-col>
      </v-row>
      <!-- NAME FIELD -->
      <validation-provider v-slot="{ errors }" name="Chapter Name">
        <v-text-field
          v-model="name"
          :error-messages="errors"
          label="Chapter Name"
          hide-details="auto"
          outlined
        ></v-text-field>
      </validation-provider>

      <v-divider class="my-3" />

      <v-btn
        v-if="chapter && !session"
        color="info"
        @click="createSession(manga_id, chapter.id)"
      >
        Edit Pages
      </v-btn>

      <page-input v-if="session" :session="session" v-model="page_order" />

      <div class="text-center mt-4">
        <v-btn type="submit" block color="background" class="text--primary">
          {{ chapter ? "Edit chapter" : "Upload chapter" }}
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script>
import { required, numeric, regex } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import Vue from "vue";
import axios from "axios";
import PageInput from "@/components/PageInput.vue";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

extend("numeric", {
  ...numeric,
  message: "{_field_} must be a number",
});

extend("regex", {
  ...regex,
  message: "{_field_} is not valid",
});

export default Vue.extend({
  name: "UploadForm",
  props: ["manga_id", "chapter"],
  components: { PageInput, ValidationProvider, ValidationObserver },
  data: () => ({
    alert: "",
    name: "",
    volume: null,
    number: null,
    session: null,
    page_order: [],
    scan_group: "no group",
  }),
  computed: {
    authConfig() {
      return this.$store.getters.authConfig;
    },
    chapter_draft() {
      return {
        name: this.name,
        number: this.number,
        volume: this.volume,
        scan_group: this.scan_group,
      };
    },
    params() {
      return {
        chapter_draft: this.chapter_draft,
        page_order: this.page_order,
      };
    },
  },
  methods: {
    async submit() {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        switch (true) {
          case this.chapter && !this.session:
            await this.editChapter(this.chapter_draft);
            break;
          case this.session && this.page_order.length > 0:
            await this.commitSession(this.params);
        }
      }
    },
    async createSession(manga_id, chapter_id) {
      let url = `/api/upload/begin`;

      const config = this.authConfig;
      config.headers["Content-Type"] = "application/json";

      const data = { manga_id, chapter_id };

      let response;
      try {
        response = await axios.post(url, data, config);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 201:
          this.session = response.data;
          break;
        case 404:
          this.alert = "Manga not found";
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
    async commitSession(params) {
      let url = `/api/upload/${this.session.id}/commit`;

      const config = this.authConfig;
      config.headers["Content-Type"] = "application/json";

      let response;
      try {
        response = await axios.post(url, params, config);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
        case 201:
          await this.$router.push(`/chapters/${response.data.id}`);
          break;
        case 404:
          await this.$router.push("/");
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
    async editChapter(chapterDraft) {
      let url = `/api/chapter/${this.chapter.id}`;

      const config = this.authConfig;
      config.headers["Content-Type"] = "application/json";

      let response;
      try {
        response = await axios.put(url, chapterDraft, config);
      } catch (e) {
        response = e.response;
      }

      switch (response.status) {
        case 200:
          await this.$router.push(`/manga/${this.manga_id}/${response.id}`);
          break;
        case 404:
          await this.$router.push("/");
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
  mounted() {
    if (this.chapter) {
      this.name = this.chapter.name;
      this.number = this.chapter.number;
      this.volume = this.chapter.volume;
      this.scan_group = this.chapter.scan_group;
    } else {
      this.createSession(this.manga_id);
    }
  },
});
</script>

<style scoped></style>
