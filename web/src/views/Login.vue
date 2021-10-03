<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk">LOGIN</v-card-title>
          <v-card-text>
            <login-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import LoginForm from '@/components/LoginForm.vue';

@Component({
  components: { LoginForm },
})
export default class Login extends Vue {
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  mounted(): void {
    if (this.isConnected) this.$router.replace('/');
  }
}
</script>
