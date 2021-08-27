<template>
  <v-container>
    <v-row class="user-row text--primary" align="center">
      <v-col class="text-center text-h5"> Username </v-col>
      <v-col class="text-center text-h5 hidden-sm-and-down"> Email </v-col>
      <v-col class="text-center text-h5"> Actions </v-col>
    </v-row>
    <v-row v-if="loading" class="user-row text--primary" align="center">
      <v-col>
        <v-skeleton-loader type="heading" class="d-flex justify-center" />
      </v-col>
      <v-col>
        <v-skeleton-loader type="heading" class="d-flex justify-center" />
      </v-col>
      <v-skeleton-loader
        width="33%"
        type="button,button"
        class="d-flex justify-space-around"
      />
    </v-row>
    <v-row
      v-else
      class="user-row text--primary"
      align="center"
      v-for="(item, index) in users"
      :key="index"
    >
      <v-col class="text-center text-body-1">
        {{ item.username }}
      </v-col>
      <v-col class="text-center text-body-1 hidden-sm-and-down">
        {{ item.email }}
      </v-col>
      <v-col class="text-center text-body-1 d-flex justify-center">
        <user-edit-button
          :user="item"
          :ownUser="userId === item.id"
          @update="update"
        />
        <user-delete-button
          :user="item"
          :disabled="userId === item.id"
          @update="update"
        />
      </v-col>
    </v-row>
    <slot />
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from "vue-property-decorator";
import UserEditButton from "@/components/UserEditButton.vue";
import UserDeleteButton from "@/components/UserDeleteButton.vue";

@Component({
  components: { UserDeleteButton, UserEditButton },
})
export default class UsersList extends Vue {
  @Prop() readonly users!: any[];
  @Prop(Boolean) readonly loading!: boolean;

  get userId(): string {
    return this.$store.getters.userId;
  }

  @Emit("update")
  update(): boolean {
    return true;
  }
}
</script>

<style lang="scss">
.user-row {
  &:first-child {
    border-radius: 0.5rem 0.5rem 0 0;
  }
  &:last-child {
    border-radius: 0 0 0.5rem 0.5rem;
  }
}

.theme--dark {
  .user-row {
    background-color: black;
    border-bottom: #212121 0.2rem solid;
  }
}
.theme--light {
  .user-row {
    background-color: #eeeeee;
    border-bottom: white 0.2rem solid;
  }
}
</style>
