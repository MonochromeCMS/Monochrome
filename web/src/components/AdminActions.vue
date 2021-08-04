<template>
  <v-list shaped>
    <v-subheader>Admin actions</v-subheader>
    <v-list-item-group v-model="selectedItem" color="primary">
      <v-list-item v-for="(item, i) in items" :key="i">
        <v-list-item-content>
          <v-list-item-title v-text="item"></v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "AdminActions",
  data: (): Record<string, any> => ({
    selectedItem: null,
    items: ["Create manga", "Handle users", "Log outq"],
  }),
});
</script>
