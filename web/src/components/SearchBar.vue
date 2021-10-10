<template>
  <div>
    <v-text-field
      hide-details
      clearable
      label="Search"
      solo
      :value="value"
      color="primary"
      background-color="background"
      :prepend-inner-icon="icons.mdiMagnify"
      dense
      @input="searchInput"
    ></v-text-field>
    <v-progress-linear indeterminate v-if="progress"></v-progress-linear>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';
import { debounce } from 'typescript-debounce-decorator';
import { mdiMagnify } from "@mdi/js";

@Component
export default class SearchBar extends Vue {
  @Prop(String) value!: string;

  icons = {
    mdiMagnify,
  };

  progress = false;

  @debounce(1200)
  _searchInput(value: string): void {
    this.$emit('input', value);
    this.$emit('update:value', value);
    this.progress = false;
  }

  searchInput(value: string): void {
    this.progress = true;
    this._searchInput(value);
  }
}
</script>
