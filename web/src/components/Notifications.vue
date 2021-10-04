<template>
  <v-snackbar
    :value="notification"
    :color="notification ? notification.color : 'error'"
    timeout="-1"
  >
    {{ notification ? `${notification.context}: ${notification.message}` : 'ERROR' }}

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
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-badge>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import type { Notification } from '@/store/notifications';

@Component
export default class ThemeToggler extends Vue {
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
