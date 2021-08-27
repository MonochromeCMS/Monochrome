<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10" md="8" lg="6" class="mx-auto">
        <v-card rounded="lg" color="backgroundAlt" elevation="0" class="pa-4">
          <v-card-title class="justify-center lemon-milk">
            CUSTOMIZE THE WEBSITE
          </v-card-title>
          <v-card-text>
            <settings-form />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import SettingsForm from "@/components/SettingsForm.vue";

@Component({
  components: { SettingsForm },
})
export default class Settings extends Vue {
  get isConnected(): boolean {
    return this.$store.getters.isConnected;
  }

  mounted(): void {
    if (!this.isConnected) this.$router.replace("/");
  }
}
</script>
