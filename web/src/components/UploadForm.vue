<template>
  <validation-observer ref="observer">
    <v-form @submit.prevent="submit">
      <v-row class="mb-3">
        <!-- VOLUME FIELD -->
        <v-col cols="12" sm="6" md="4" class="pa-3 pb-0">
          <validation-provider v-slot="{ errors }" name="Volume Number" rules="numeric">
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
          <validation-provider v-slot="{ errors }" name="Scan Group" rules="required">
            <v-combobox
              v-model="scanGroup"
              :items="groupAutocomplete"
              :error-messages="errors"
              label="Scan Group"
              outlined
              hide-details="auto"
            />
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

      <!-- NAME FIELD -->
      <validation-provider v-slot="{ errors }" name="Webtoon">
        <v-checkbox
          v-model="webtoon"
          :error-messages="errors"
          label="This chapter is a webtoon (the webtoon reader will be used)"
          hide-details="auto"
        ></v-checkbox>
      </validation-provider>

      <v-divider class="my-3" />

      <v-btn v-if="chapter && !session" color="info" @click="createSession(mangaId, chapter.id)">
        Edit Pages
      </v-btn>

      <page-input v-if="session" :session="session" v-model="pageOrder" />

      <div class="text-center mt-4">
        <v-btn type="submit" block color="background" class="text--primary">
          {{ chapter ? 'Edit chapter' : 'Upload chapter' }}
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { required, numeric, regex } from 'vee-validate/dist/rules';
import { extend, ValidationProvider, setInteractionMode, ValidationObserver } from 'vee-validate';
import { Vue, Component, Prop } from 'vue-property-decorator';
import type { AxiosRequestConfig } from 'axios';
import PageInput from '@/components/PageInput.vue';
import type { UploadSessionResponse } from '@/api/Upload';
import Upload from '@/api/Upload';
import type { ChapterSchema } from '@/api/Chapter';
import Chapter from '@/api/Chapter';
import Autocomplete from '@/api/Autocomplete';

setInteractionMode('eager');

extend('required', {
  ...required,
  message: '{_field_} can not be empty',
});

extend('numeric', {
  ...numeric,
  message: '{_field_} must be a number',
});

extend('regex', {
  ...regex,
  message: '{_field_} is not valid',
});

@Component({
  components: { PageInput, ValidationProvider, ValidationObserver },
})
export default class UploadForm extends Vue {
  @Prop(String) readonly mangaId!: string;

  @Prop() readonly chapter!: any;

  groupAutocomplete: string[] = [];

  name = '';

  volume = null;

  number = null;

  webtoon = false;

  session: UploadSessionResponse | null = null;

  pageOrder: string[] = [];

  scanGroup = 'no group';

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  get chapterDraft(): ChapterSchema {
    return {
      name: this.name,
      number: this.number ?? 0,
      volume: this.volume ?? undefined,
      webtoon: this.webtoon,
      scanGroup: this.scanGroup,
    };
  }

  async submit(): Promise<void> {
    //@ts-expect-error I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      switch (true) {
        case this.chapter && !this.session:
          await this.editChapter(this.chapterDraft);
          break;
        case this.session && this.pageOrder.length > 0:
          await this.commitSession(this.chapterDraft, this.pageOrder);
      }
    }
  }

  async createSession(mangaId: string, chapter: string | null): Promise<void> {
    const config = this.authConfig;
    const response = await Upload.begin(mangaId, chapter, config);

    if (response.data) {
      this.session = response.data;
    } else {
      const notification = {
        context: 'Create upload session',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
    if (response.status === 401) {
      this.$store.commit('logout');
    }
  }

  async commitSession(chapterDraft: ChapterSchema, pageOrder: string[]): Promise<void> {
    if (!this.session?.id) {
      return;
    }

    const config = this.authConfig;
    const response = await Upload.commit(this.session.id, chapterDraft, pageOrder, config);

    if (response.data) {
      await this.$router.push(`/chapters/${response.data.id}`);
    } else {
      const notification = {
        context: 'Commit upload session',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
    if (response.status === 401) {
      this.$store.commit('logout');
    }
  }

  async editChapter(chapterDraft: ChapterSchema): Promise<void> {
    const response = await Chapter.edit(this.chapter.id, chapterDraft, this.authConfig);

    if (response.data) {
      await this.$router.push(`/manga/${this.mangaId}/${response.data.id}`);
    } else {
      const notification = {
        context: 'Edit settings',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
    if (response.status === 401) {
      this.$store.commit('logout');
    }
  }

  async autocomplete(): Promise<void> {
    const response = await Autocomplete.groups();

    if (response.data) {
      this.groupAutocomplete = response.data;
    } else {
      const notification = {
        context: 'Group autocomplete',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
  }

  mounted(): void {
    if (this.chapter) {
      this.name = this.chapter.name;
      this.number = this.chapter.number;
      this.volume = this.chapter.volume;
      this.webtoon = this.chapter.webtoon;
      this.scanGroup = this.chapter.scanGroup;
    } else {
      this.createSession(this.mangaId, null);
    }
    this.autocomplete();
  }
}
</script>
