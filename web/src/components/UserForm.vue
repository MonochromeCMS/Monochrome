<template>
  <validation-observer ref="observer">
    <v-form @submit.prevent="submit">
      <v-card color="background">
        <v-card-title> {{ user ? 'Edit' : 'Add' }} user </v-card-title>
        <v-alert type="warning" v-if="ownUser" dense class="ma-3">
          You'll be logged out after editing your own user !
        </v-alert>
        <v-card-text>
          <validation-provider v-slot="{ errors }" name="Username" rules="required|max:15">
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
            ></v-text-field>
          </validation-provider>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <slot />
          <v-btn color="gray" text @click="close"> Cancel </v-btn>
          <v-btn :disabled="loading" type="submit" color="green" class="text--white">
            {{ user ? 'EDIT' : 'ADD' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </validation-observer>
</template>

<script lang="ts">
import { required, email, max } from 'vee-validate/dist/rules';
import { extend, ValidationProvider, setInteractionMode, ValidationObserver } from 'vee-validate';
import { Vue, Component, Emit, Prop } from 'vue-property-decorator';
import User from '@/api/User';
import { mdiEye, mdiEyeOff } from "@mdi/js";
import type { AxiosRequestConfig } from 'axios';
import type { UserSchema } from '@/api/User';

setInteractionMode('eager');

extend('max', {
  ...max,
  message: "{_field_} can't be that long",
});

extend('email', {
  ...email,
  message: '{_field_} must be a valid email',
});

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
export default class UserForm extends Vue {
  @Prop() readonly user!: any;

  @Prop(Boolean) readonly ownUser!: boolean;

  icons = {
    mdiEye,
    mdiEyeOff,
  };

  username = '';

  password = '';

  email = null;

  showPass = false;

  loading = false;

  mounted(): void {
    if (this.user) {
      this.username = this.user.username;
      this.password = this.user.password;
      this.email = this.user.email;
    }
  }

  get params(): any {
    return {
      username: this.username,
      password: this.password,
      email: this.email || undefined,
    };
  }

  get authConfig(): AxiosRequestConfig {
    return this.$store.getters.authConfig;
  }

  @Emit('close')
  close(): boolean {
    return true;
  }

  async submit(): Promise<void> {
    //@ts-expect-error I can't define this $ref, so let's assume it works
    const valid = await this.$refs.observer.validate();
    if (valid) {
      if (this.user) {
        await this.editUser(this.user.id, this.params);
      } else {
        await this.addUser(this.params);
      }
    }
  }

  clear(): void {
    this.username = '';
    this.email = null;
    this.password = '';
  }

  async editUser(userId: string, params: UserSchema): Promise<void> {
    this.loading = true;
    const response = await User.edit(userId, params, this.authConfig);

    if (response.data) {
      this.$emit('update', true);
      this.close();
    } else {
      const notification = {
        context: 'Edit user',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
    if (response.status === 401) {
      this.$store.commit('logout');
    }

    this.loading = false;
  }

  async addUser(params: UserSchema): Promise<void> {
    this.loading = true;
    const response = await User.create(params, this.authConfig);

    if (response.data) {
      this.$emit('update', true);
      this.clear();
      this.close();
    } else {
      const notification = {
        context: 'Create user',
        message: response.error ?? '',
        color: 'error',
      };
      await this.$store.dispatch('pushNotification', notification);
    }
    if (response.status === 401) {
      this.$store.commit('logout');
    }

    this.loading = false;
  }
}
</script>
