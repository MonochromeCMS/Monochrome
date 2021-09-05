<template>
  <v-dialog v-model="dialog" max-width="30rem" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        :disabled="disabled"
        class="mx-2"
        width="3rem"
        color="error"
        v-bind="attrs"
        v-on="on"
        aria-label="Delete user"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="text-h5 background mb-2"> Warning </v-card-title>
      <v-alert type="error" v-if="alert !== ''" dense class="ma-3">
        {{ alert }}
      </v-alert>
      <v-card-text class="body-1">
        <span class="font-weight-bold">This action can't be undone!</span>
        Are you sure you want to delete this user?
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray" text @click="dialog = false"> Cancel </v-btn>
        <v-btn color="error" @click="deleteUser(user.id)" :loading="loading">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from "vue-property-decorator";
import User from "@/api/User";
import type {AxiosRequestConfig} from "axios";

@Component
export default class UserDeleteButton extends Vue {
  @Prop() readonly user!: any;
  @Prop(Boolean) readonly disabled!: boolean;

  loading = false;
  dialog = false;
  alert = "";

  @Emit("update")
  update(): boolean {
    return true;
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  async deleteUser(userId: string): Promise<void> {
    this.loading = true;
    const response = await User.delete(userId, this.authConfig);

    if (response.data) {
      this.$emit("update", true);
      this.dialog = false;
    } else {
      this.alert = response.error ?? "";
    }
    if (response.status === 401) {
      this.$store.commit("logout");
    }
    this.loading = false;
  }
}
</script>
