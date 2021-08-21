<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10" md="8" lg="6" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk"
            >CUSTOMIZE THE WEBSITE</v-card-title
          >
          <v-card-text>
            <settings-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script type="ts">
import Vue from "vue";
import SettingsForm from "@/components/SettingsForm.vue";

export default Vue.extend({
  components: {SettingsForm},
  computed: {
    isConnected() {
      return this.$store.getters.isConnected;
    }
  },
  mounted() {
    if (!this.isConnected) this.$router.replace("/");
  },
});
</script>
