<template>
  <v-container>
    <h3>Pages</h3>
    <v-alert v-if="alert !== ''" type="error">{{ alert }}</v-alert>
    <draggable class="drag-pages" v-model="pages">
      <template v-for="(item, index) in pages">
        <v-col cols="6" sm="4" md="3" xl="2" :key="index">
          <v-card color="background" class="page-card">
            <v-img
              :src="`/media/blobs/${item.id}.jpg`"
              :aspect-ratio="4 / 5"
              position="relative"
            >
              <v-btn
                icon
                class="background text--primary page-close"
                @click="deletePage(index, item.id)"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-chip class="page-name">{{ item.name }}</v-chip>
            </v-img>
          </v-card>
        </v-col>
      </template>
      <v-col cols="6" sm="4" md="3" xl="2">
        <v-card color="background" @click="uploadClick" :loading="!!loading">
          <v-responsive :aspect-ratio="4 / 5">
            <div class="d-flex fill-height">
              <v-icon x-large class="ma-auto d-block">mdi-plus</v-icon>
            </div>
          </v-responsive>
        </v-card>
      </v-col>
    </draggable>
    <v-btn text @click="quickSort"> Quick sort </v-btn>
    <input
      ref="fileInput"
      type="file"
      @input="updateFile"
      multiple
      style="display: none"
    />
    <div>
      <ul>
        <li>Supported image formats are JPEG, PNG, GIF, BMP and WebP.</li>
        <li>You can upload multiple images at the same time.</li>
      </ul>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Prop, VModel, Watch } from "vue-property-decorator";
import draggable from "vuedraggable";
import axios, { AxiosRequestConfig } from "axios";
import naturalCompare from "natural-compare-lite";

@Component({
  components: { draggable },
})
export default class PageInput extends Vue {
  $refs!: {
    fileInput: HTMLInputElement;
  };

  @Prop() readonly session!: any;

  @VModel() pageOrder!: any[];

  pages: any[] = [];
  loading = 0;
  pageUpload = null;
  alert = "";

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  mounted(): void {
    this.pages = this.session.blobs;
  }

  @Watch("pages")
  onPagesChange(value: any[]): void {
    this.pageOrder = value.map((el) => el.id);
  }

  uploadClick(): void {
    this.$refs.fileInput.click();
  }

  async updateFile(ev: any): Promise<void> {
    if (!ev.target) {
      return;
    }

    await this.uploadFiles(ev.target.files);
    ev.target.value = null;
  }

  async uploadFiles(files: File[]): Promise<void> {
    let url = `/api/upload/${this.session.id}`;

    this.loading += 1;

    const config = this.authConfig;
    config.headers["Content-Type"] = "text";

    const form = new FormData();
    files.forEach((file) => form.append("payload", file));

    let response;
    try {
      response = await axios.post(url, form, config);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 201:
        this.pages = this.pages.concat(response.data);
        break;
      case 404:
        this.alert = "Session not found";
        break;
      case 422:
        this.alert = "The ID provided isn't an UUID";
        break;
      case 401:
        this.$store.commit("logout");
        break;
      default:
        this.alert = response.statusText;
    }

    this.loading -= 1;
  }

  async deletePage(index: number, id: string): Promise<void> {
    let url = `/api/upload/${this.session.id}/${id}`;

    const config = this.authConfig;

    let response;
    try {
      response = await axios.delete(url, config);
    } catch (e) {
      response = e.response;
    }

    switch (response.status) {
      case 200:
      case 404:
        this.pages = this.pages
          .slice(0, index)
          .concat(this.pages.slice(index + 1));
        break;
      case 401:
        this.$store.commit("logout");
        break;
      default:
        this.alert = response.statusText;
    }
  }

  quickSort(): void {
    this.pages = this.pages
      .slice()
      .sort((a, b) => naturalCompare(a.name, b.name));
  }
}
</script>

<style scoped>
.page-card {
  cursor: grab;
}
.page-name {
  position: absolute;
  bottom: 0.1rem;
  left: 0.1rem;
}
.page-close {
  position: absolute;
  right: 0.1rem;
  top: 0.1rem;
}
.drag-pages {
  display: flex;
  flex-wrap: wrap;
}
</style>
