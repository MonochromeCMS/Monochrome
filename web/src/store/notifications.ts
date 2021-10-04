export interface NotificationInput {
  color: 'success' | 'error' | 'warning';
  message: string;
  context: string;
}

export interface Notification {
  color: string;
  message: string;
  context: string;
}

interface NotificationsState {
  notifications: Notification[];
}

const colors = {
  success: 'success black--text',
  error: 'error white--text',
  warning: 'warning black--text',
};

const state = (): NotificationsState => ({
  notifications: [],
});

const getters = {
  getNotification(state: NotificationsState): Notification | null {
    const length = state.notifications.length;
    return length > 0 ? state.notifications[length - 1] : null;
  },
  notificationsAmount(state: NotificationsState): number {
    return state.notifications.length;
  },
};

const mutations = {
  closeNotification(state: NotificationsState): void {
    if (state.notifications.length > 0) {
      state.notifications = state.notifications.slice(0, -1);
    }
  },
  addNotification(state: NotificationsState, payload: NotificationInput): void {
    const notification = { ...payload, color: colors[payload.color] };
    state.notifications = state.notifications.concat([notification]);
  },
};

export default {
  state,
  getters,
  mutations,
};
