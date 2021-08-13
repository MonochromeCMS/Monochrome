<template>
  <validation-observer ref="observer">
    <v-form @submit.prevent="submit">
      <v-card color="background">
        <v-card-title> {{ user ? "Edit" : "Add" }} user </v-card-title>
        <v-alert type="warning" v-if="ownUser" dense class="ma-3">
          You'll be logged out after editing your own user !
        </v-alert>
        <v-alert type="error" v-if="alert !== ''" dense class="ma-3">
          {{ alert }}
        </v-alert>
        <v-card-text>
          <validation-provider
            v-slot="{ errors }"
            name="Username"
            rules="required|max:15"
          >
            <v-text-field
              v-model="username"
              :error-messages="errors"
              label="Username"
              required
              outlined
            ></v-text-field>
          </validation-provider>
          <validation-provider v-slot="{ errors }" name="Email" rules="email">
            <v-text-field
              v-model="email"
              :error-messages="errors"
              label="Email"
              outlined
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="Password"
            rules="required"
          >
            <v-text-field
              v-model="password"
              :error-messages="errors"
              label="Password"
              :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPass = !showPass"
              required
              outlined
              :type="showPass ? 'text' : 'password'"
            ></v-text-field>
          </validation-provider>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <slot />
          <v-btn color="gray" text @click="close"> Cancel </v-btn>
          <v-btn
            :disabled="loading"
            type="submit"
            color="green"
            class="text--white"
          >
            {{ user ? "EDIT" : "ADD" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </validation-observer>
</template>

<script>
import { required, email, max } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import Vue from "vue";

setInteractionMode("eager");

extend("max", {
  ...max,
  message: "{_field_} can't be that long",
});

extend("email", {
  ...email,
  message: "{_field_} must be a valid email",
});

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

export default Vue.extend({
  name: "LoginForm",
  props: ["user", "ownUser"],
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    username: "",
    password: "",
    email: null,
    showPass: false,
    alert: "",
    loading: false,
  }),
  mounted() {
    if (this.user) {
      this.username = this.user.username;
      this.password = this.user.password;
      this.email = this.user.email;
    }
  },
  computed: {
    params() {
      return {
        username: this.username,
        password: this.password,
        email: this.email || undefined,
      };
    },
  },
  methods: {
    close() {
      this.$emit("close", true);
    },
    async submit() {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        if (this.user) {
          await this.editUser(this.user.id, this.params);
        } else {
          await this.addUser(this.params);
        }
      }
    },
    clear() {
      this.alert = "";
      this.username = "";
      this.email = null;
      this.password = "";
      this.$refs.observer.reset();
    },
    async editUser(user_id, params) {
      this.loading = true;
      const response = await this.$store.dispatch("editUser", [
        user_id,
        params,
      ]);

      switch (response.status) {
        case 200:
          this.$emit("update", true);
          this.close();
          break;
        default:
          this.alert = response.data.detail || response.statusText;
      }
      this.loading = false;
    },
    async addUser(params) {
      this.loading = true;
      const response = await this.$store.dispatch("createUser", params);

      switch (response.status) {
        case 201:
          this.$emit("update", true);
          this.clear();
          this.close();
          break;
        default:
          this.alert = response.data.detail || response.statusText;
      }
      this.loading = false;
    },
  },
});
</script>
