<template>
  <div>
    <v-text-field
      hide-details
      clearable
      solo
      :value="value"
      color="primary"
      background-color="background"
      prepend-inner-icon="mdi-magnify"
      dense
      @input="searchInput"
    ></v-text-field>
    <v-progress-linear indeterminate v-if="progress"></v-progress-linear>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import _debounce from "lodash/debounce";

export default Vue.extend({
  name: "SearchBar",
  props: ["value"],
  data: () => ({
    progress: false,
  }),
  methods: {
    _searchInput: _debounce(function (value: string) {
      this.$emit("input", value);
      this.$emit("update:value", value);
      this.progress = false;
    }, 1200),
    searchInput(value: string) {
      this.progress = true;
      this._searchInput(value);
    },
  },
});
</script>

<style scoped></style>
