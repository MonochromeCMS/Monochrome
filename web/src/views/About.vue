<template>
  <v-container>
    <v-row>
      <v-col class="mx-auto" cols="12" md="10" lg="8" xl="6">
        <v-card
          rounded="lg"
          color="backgroundAlt"
          elevation="0"
          class="text-center"
        >
          <template v-if="settings.about">
            <div class="pt-3 px-3" v-html="markdownHTML" />
            <v-card-actions>
              <div class="caption ml-auto text--secondary">
                This website was created with
                <a
                  href="https://github.com/D34DPlayer/Monochrome"
                  class="text-decoration-none"
                  target="_blank"
                >
                  Monochrome </a
                >.
              </div>
            </v-card-actions>
          </template>

          <template v-else>
            <v-card-title class="justify-center lemon-milk">
              About us
            </v-card-title>
            <v-card-text class="text-center text-body-1">
              <v-row>
                <v-col cols="12">
                  This website was created with
                  <a
                    href="https://github.com/D34DPlayer/Monochrome"
                    class="text-decoration-none"
                    target="_blank"
                  >
                    Monochrome </a
                  >.
                </v-col>
                <v-col cols="12">
                  Monochrome's goal is to provide a good quality manga CMS for
                  anyone to host.
                </v-col>
                <v-col cols="12">
                  You can find how it works and how to set up your own version
                  of Monochrome on
                  <a
                    href="https://github.com/D34DPlayer/Monochrome"
                    class="text-decoration-none"
                    target="_blank"
                  >
                    Github </a
                  >.
                </v-col>
                <v-col cols="12" class="mb-2">
                  And if you are interested, you can find more about its creator
                  <a
                    href="https://www.d34d.one"
                    class="text-decoration-none"
                    target="_blank"
                  >
                    here </a
                  >.
                </v-col>
              </v-row>
            </v-card-text>
          </template>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import marked from "marked";
import { SettingsSchema } from "@/api/Settings";

@Component
export default class About extends Vue {
  get markdownHTML() {
    return this.settings.about ? marked(this.settings.about) : "";
  }

  get settings(): SettingsSchema {
    return this.$store.getters.settings;
  }
}
</script>
