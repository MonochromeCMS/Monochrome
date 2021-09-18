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
        Markdown (or HTML) can be used to customize the About page. More
        information in the
        <a
          href="https://www.markdownguide.org/basic-syntax"
          class="text-decoration-none"
        >
          Markdown documentation </a
        >.
      </div>

      <!-- PREVIEW -->
      <v-expansion-panels class="mb-4">
        <v-expansion-panel>
          <v-expansion-panel-header> Preview </v-expansion-panel-header>
          <v-expansion-panel-content class="text-center">
            <div v-html="markdownHTML" />
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

<script lang="ts">
import {
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import { Vue, Component, Watch } from "vue-property-decorator";
import marked from "marked";
import Settings, { SettingsSchema } from "@/api/Settings";
import type { AxiosRequestConfig } from "axios";

setInteractionMode("eager");

@Component({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
})
export default class SettingsForm extends Vue {
  title1?: string | null = null;
  title2?: string | null = null;
  about?: string | null = null;
  success = false;
  alert = "";

  get params(): any {
    return {
      title1: this.title1 || null,
      title2: this.title2 || null,
      about: this.about || null,
    };
  }

  get markdownHTML() {
    return this.about ? marked(this.about) : "";
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  get settings(): SettingsSchema {
    return this.$store.getters.settings;
  }

  async submit(): Promise<void> {
    //@ts-ignore I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      await this.editSettings(this.params);
    }
  }
  async editSettings(params: SettingsSchema): Promise<void> {
    this.success = false;

    const response = await Settings.edit(params, this.authConfig);

    if (response.data) {
      this.$store.commit("setSettings", response.data);
      this.success = true;
    } else {
      this.alert = response.error ?? "";
    }
    if (response.status === 401) {
      this.$store.commit("logout");
    }
  }

  @Watch("settings")
  onSettingsUpdate(value: any): void {
    this.title1 = value.title1;
    this.title2 = value.title2;
    this.about = value.about;
  }

  mounted(): void {
    this.title1 = this.settings.title1;
    this.title2 = this.settings.title2;
    this.about = this.settings.about;
  }
}
</script>
