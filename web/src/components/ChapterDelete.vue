<template>
  <v-dialog v-model="dialog" max-width="30rem">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="error" block v-bind="attrs" v-on="on"> Delete Chapter </v-btn>
    </template>

    <v-card>
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

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';
import type { AxiosRequestConfig } from 'axios';
import Chapter from '@/api/Chapter';

@Component
export default class ChapterDelete extends Vue {
  dialog = false;

  @Prop() readonly id!: string;

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  async deleteChapter(): Promise<void> {
    const response = await Chapter.delete(this.id, this.authConfig);

    if (response.data) {
      this.$emit('input', true);
      this.dialog = false;
    } else {
      const notification = {
        context: 'Delete chapter',
        message: response.error ?? '',
        color: 'error',
      };
      this.$store.commit('addNotification', notification);
    }

    if (response.status === 401) {
      this.$store.commit('logout');
    }
  }
}
</script>
