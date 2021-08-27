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
import { Vue, Component, Prop } from "vue-property-decorator";
import { debounce } from "typescript-debounce-decorator";

@Component
export default class SearchBar extends Vue {
  @Prop(String) value!: string;

  progress = false;

  @debounce(1200)
  _searchInput(value: string): void {
    this.$emit("input", value);
    this.$emit("update:value", value);
    this.progress = false;
  }

  searchInput(value: string): void {
    this.progress = true;
    this._searchInput(value);
  }
}
</script>
