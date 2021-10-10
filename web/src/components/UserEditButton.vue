<template>
  <v-dialog v-model="dialog" max-width="30rem" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn class="mx-2" width="3rem" color="info" v-bind="attrs" v-on="on" aria-label="Edit user">
        <v-icon>{{ icons.mdiPencil }}</v-icon>
      </v-btn>
    </template>
    <user-form :user="user" @close="dialog = false" :ownUser="ownUser" @update="update" />
  </v-dialog>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator';
import UserForm from './UserForm.vue';
import { mdiPencil } from '@mdi/js';

@Component({
  components: { UserForm },
})
export default class UserEditButton extends Vue {
  @Prop() readonly user!: any;

  @Prop(Boolean) readonly ownUser!: boolean;

  icons = {
    mdiPencil,
  };

  dialog = false;

  @Emit('update')
  update(): boolean {
    return true;
  }
}
</script>
