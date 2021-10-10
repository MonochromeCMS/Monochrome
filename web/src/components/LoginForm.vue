<template>
  <validation-observer ref="observer">
    <v-form @submit.prevent="submit">
      <validation-provider v-slot="{ errors }" name="Username/email" rules="required">
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
          :append-icon="showPass ? icons.mdiEye : icons.mdiEyeOff"
          @click:append="showPass = !showPass"
          required
          outlined
          :type="showPass ? 'text' : 'password'"
        />
      </validation-provider>
      <div class="text-center">
        <v-btn type="submit" block color="background" class="text--primary"> Sign In </v-btn>
      </div>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { required } from 'vee-validate/dist/rules';
import { extend, ValidationProvider, setInteractionMode, ValidationObserver } from 'vee-validate';
import { mdiEye, mdiEyeOff } from "@mdi/js";

setInteractionMode('eager');

extend('required', {
  ...required,
  message: '{_field_} can not be empty',
});

@Component({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
})
export default class LoginForm extends Vue {
  icons = {
    mdiEye,
    mdiEyeOff,
  };

  username = '';

  password = '';

  showPass = false;

  get params(): any {
    return {
      username: this.username,
      password: this.password,
    };
  }

  async submit(): Promise<void> {
    //@ts-expect-error I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      await this.login(this.params); // action to login
    }
  }

  clear(): void {
    this.username = '';
    this.password = '';
  }

  async login(params: any): Promise<void> {
    const response = await this.$store.dispatch('login', params);

    if (response.data) {
      this.clear();
    } else {
      const notification = {
        context: 'Login',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
  }
}
</script>
