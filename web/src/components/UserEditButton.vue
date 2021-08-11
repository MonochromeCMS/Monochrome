<template>
  <v-dialog v-model="dialog" max-width="30rem" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn class="mx-2" width="3rem" color="info" v-bind="attrs" v-on="on">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </template>
    <user-form
      :user="user"
      @close="dialog = false"
      :ownUser="ownUser"
      @update="update"
    />
  </v-dialog>
</template>

<script>
import Vue from "vue";
import UserForm from "./UserForm";

export default Vue.extend({
  name: "UserEditButton",
  components: { UserForm },
  props: ["user", "ownUser"],
  data: () => ({
    dialog: false,
  }),
  methods: {
    update() {
      this.$emit("update", true);
    },
  },
});
</script>
