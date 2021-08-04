<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4" class="align-center mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center login-title">LOGIN</v-card-title>
          <v-card-text>
            <login-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import LoginForm from "@/components/LoginForm.vue";

export default Vue.extend({
  name: "Login",
  components: {
    LoginForm,
  },
});
</script>

<style lang="scss">
.login-title {
  font-family: LemonMilk, Roboto, serif;
}
</style>