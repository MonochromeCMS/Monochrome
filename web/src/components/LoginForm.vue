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
        />
      </validation-provider>
      <validation-provider v-slot="{ errors }" name="Password" rules="required">
        <v-text-field
          v-model="password"
          :error-messages="errors"
          label="Password"
          :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPass = !showPass"
          required
          outlined
          :type="showPass ? 'text' : 'password'"
        />
      </validation-provider>
      <div class="text-center">
        <v-btn type="submit" block color="background" class="text--primary">
          Sign In
        </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { required } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  setInteractionMode,
  ValidationObserver,
} from "vee-validate";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

@Component({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
})
export default class LoginForm extends Vue {
  username = "";
  password = "";
  showPass = false;
  alert = "";

  get params(): any {
    return {
      username: this.username,
      password: this.password,
    };
  }

  async submit(): Promise<void> {
    //@ts-ignore I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      await this.login(this.params); // action to login
    }
  }

  clear(): void {
    this.alert = "";
    this.username = "";
    this.password = "";
  }

  async login(params: any): Promise<void> {
    const response = await this.$store.dispatch("login", params);

    switch (response.status) {
      case 200:
        this.clear();
        break;
      default:
        this.alert = response.data.detail ?? response.statusText;
    }
  }
}
</script>
