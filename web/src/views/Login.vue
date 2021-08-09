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

<script>
import Vue from "vue";
import LoginForm from "@/components/LoginForm.vue";

export default Vue.extend({
  name: "Login",
  components: {
    LoginForm,
  },
  computed: {
    isConnected() {
      return this.$store.getters.isConnected;
    },
  },
  mounted() {
    if (this.isConnected) this.$router.replace("/");
  },
});
</script>

<style lang="scss"></style>
