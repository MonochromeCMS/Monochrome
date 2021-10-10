<template>
  <v-snackbar :value="notificationsAmount" :color="notification ? notification.color : 'info'">
    {{
      notification ? `${notification.context}: ${notification.message}` : 'No notifications left'
    }}

    <template v-slot:action="{ attrs }">
      <v-badge
        color="black"
        :content="notificationsAmount"
        :value="notificationsAmount"
        overlap
        offset-x="1.5rem"
        offset-y="1rem"
      >
        <v-btn dark text v-bind="attrs" @click="close">
          <v-icon>{{ icons.mdiClose }}</v-icon>
        </v-btn>
      </v-badge>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiClose } from '@mdi/js';
import type { Notification } from '@/store/notifications';

@Component
export default class ThemeToggler extends Vue {
  icons = {
    mdiClose,
  };

  close(): void {
    this.$store.commit('closeNotification');
  }

  get notification(): Notification {
    return this.$store.getters.getNotification;
  }

  get notificationsAmount(): number {
    return this.$store.getters.notificationsAmount;
  }
}
</script>

<style lang="scss"></style>
