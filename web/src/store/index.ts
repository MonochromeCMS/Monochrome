import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

import notifications from './notifications';
import user from './user';
import reader from './reader';
import settings from './settings';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { notifications, user, reader, settings },
  plugins: [createPersistedState()],
});
