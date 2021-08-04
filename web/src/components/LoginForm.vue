<template>
  <validation-observer ref="observer">
    <v-alert type="error" v-if="alert !== ''" dense class="mb-7">
      {{ alert }}
    </v-alert>
    <v-form @submit.prevent="submit">
      <validation-provider
        v-slot="{ errors }"
        name="Username/email"
        rules="required"
      >
        <v-text-field
          v-model="username"
          :error-messages="errors"
          label="Username/email"
          required
          outlined
        ></v-text-field>
      </validation-provider>
      <validation-provider v-slot="{ errors }" name="email" rules="required">
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
      <div class="text-center">
        <v-btn type="submit" block color="background" class="text--primary"> Sign In </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { required } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";
import Vue from "vue";
import type { UserLogin } from "@/store/user";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

export default Vue.extend({
  name: "LoginForm",
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    username: "",
    password: "",
    showPass: false,
    alert: "",
  }),
  computed: {
    params(): UserLogin {
      return {
        username: this.username,
        password: this.password,
      };
    },
  },
  methods: {
    async submit(): Promise<void> {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        await this.login(this.params); // action to login
      }
    },
    clear(): void {
      this.alert= "";
      this.username = "";
      this.password = null;
      this.$refs.observer.reset();
    },
    async login(params: UserLogin): Promise<void> {
      const response = await this.$store.dispatch("login", params);
      console.log(response);
      //TODO: Check the status, show error if needed
      switch (response.status) {
        case 200:
          this.clear();
          break;
        default:
          this.alert = response.statusText;
      }
    },
  },
});
</script>
