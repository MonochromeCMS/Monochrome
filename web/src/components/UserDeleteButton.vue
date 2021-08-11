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
        <v-btn color="error" @click="deleteUser(user.id)"> Delete </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  name: "UserDeleteButton",
  props: ["user", "disabled"],
  data: () => ({
    dialog: false,
    alert: "",
  }),
  methods: {
    update() {
      this.$emit("update", true);
    },
    async deleteUser(user_id) {
      this.loading = true;
      const response = await this.$store.dispatch("deleteUser", user_id);

      switch (response.status) {
        case 200:
          this.$emit("update", true);
          this.dialog = false;
          break;
        default:
          this.alert = response.data.detail || response.statusText;
      }
      this.loading = false;
    },
  },
});
</script>
