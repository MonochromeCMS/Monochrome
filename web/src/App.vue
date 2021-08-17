<template>
  <v-app id="monochrome" class="v-application">
    <nav-bar />
    <v-main class="background">
      <router-view />
    </v-main>
    <theme-toggler />
  </v-app>
</template>

<script>
import Vue from "vue";
import NavBar from "./components/NavBar.vue";
import ThemeToggler from "@/components/ThemeToggler.vue";

export default Vue.extend({
  name: "App",

  components: {
    ThemeToggler,
    NavBar,
  },
  metaInfo() {
    const protocol = process.env.VUE_APP_PROTOCOL || "http";
    const domain = process.env.VUE_APP_DOMAIN_NAME || "localhost";
    const title = process.env.VUE_APP_TITLE || "Monochrome";
    const description = process.env.VUE_APP_DESCRIPTION || "A website for reading manga";
    return {
      title,
      titleTemplate: `%s | ${title}`,
      meta: [
        {
          property: "twitter:title",
          content: title,
        },
        {
          vmid: "title",
          property: "og:title",
          content: title,
        },
        {
          property: "twitter:card",
          content: "summary",
        },
        {
          property: "og:type",
          content: "website",
        },
        {
          property: "og:image",
          content: `${protocol}://${domain}/img/icons/android-chrome-512x512.png`,
        },
        {
          property: "twitter:image",
          content: `${protocol}://${domain}/img/icons/android-chrome-512x512.png`,
        },
        {
          property: "og:url",
          content: `${protocol}://${domain}`,
        },
        {
          property: "og:description",
          content: description,
        },
        {
          property: "twitter:description",
          content: description,
        },
        {
          name: "description",
          content: description,
        },
        {
          property: "og:locale",
          content: "en_US",
        },
      ],
    };
  },
  computed: {
    isConnected: function () {
      return this.$store.getters.isConnected;
    },
  },
  watch: {
    isConnected: function () {
      this.$router.replace("/");
    },
  },
  mounted() {
    if (this.isConnected) this.$store.dispatch("getUserData");
  },
});
</script>

<style lang="scss">
.v-application {
  font-family: Roboto, serif;
}
</style>
