<template>
  <validation-observer ref="observer">
    <v-alert type="success" v-if="success" dense>
      The settings have been updated.
    </v-alert>
    <v-alert type="error" v-else-if="alert !== ''" dense>
      {{ alert }}
    </v-alert>
    <v-form @submit.prevent="submit">
      <!-- TITLE FIELD -->
      <v-row>
        <v-col cols="12" md="6">
          <validation-provider v-slot="{ errors }" name="Title(first part)">
            <v-text-field
              v-model="title1"
              :error-messages="errors"
              label="Title(first part)"
              outlined
            ></v-text-field>
          </validation-provider>
        </v-col>
        <v-col cols="12" md="6">
          <validation-provider v-slot="{ errors }" name="Title(second part)">
            <v-text-field
              v-model="title2"
              :error-messages="errors"
              label="Title(second part)"
              outlined
            ></v-text-field>
          </validation-provider>
        </v-col>
      </v-row>
      <!-- ABOUT FIELD -->
      <validation-provider v-slot="{ errors }" name="About page">
        <v-textarea
          v-model="about"
          :error-messages="errors"
          label="About page"
          hide-details="auto"
          outlined
        ></v-textarea>
      </validation-provider>

      <div class="caption ma-3">
        Markdown (or HTML) can be used to customize the About page. You can find
        its syntax
        <a
          href="https://www.markdownguide.org/basic-syntax"
          class="text-decoration-none"
          >here</a
        >.
      </div>

      <!-- PREVIEW -->
      <v-expansion-panels class="mb-4">
        <v-expansion-panel>
          <v-expansion-panel-header> Preview </v-expansion-panel-header>
          <v-expansion-panel-content class="text-center">
            <vue-markdown :source="about" />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
      <div class="text-center">
        <v-btn type="submit" block color="background" class="text--primary">
          Customize
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script>
import {
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import Vue from "vue";
import VueMarkdown from "vue-markdown";

setInteractionMode("eager");

export default Vue.extend({
  name: "SettingsForm",
  components: {
    VueMarkdown,
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    title1: null,
    title2: null,
    about: null,
    success: false,
    alert: "",
  }),
  computed: {
    params() {
      return {
        title1: this.title1 || null,
        title2: this.title2 || null,
        about: this.about || null,
      };
    },
    settings() {
      return this.$store.getters.settings;
    },
  },
  methods: {
    async submit() {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        await this.editSettings(this.params);
      }
    },
    async editSettings(params) {
      this.success = false;

      const response = await this.$store.dispatch("editSettings", params);

      switch (response.status) {
        case 200:
          this.success = true;
          break;
        case 401:
          break;
        default:
          this.alert = response.statusText;
      }
    },
  },
  watch: {
    settings(value) {
      this.title1 = value.title1;
      this.title2 = value.title2;
      this.about = value.about;
    },
  },
  mounted() {
    this.title1 = this.settings.title1;
    this.title2 = this.settings.title2;
    this.about = this.settings.about;
  },
});
</script>
