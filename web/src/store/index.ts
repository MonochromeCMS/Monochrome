import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import SecureLS from 'secure-ls';

const ls = new SecureLS({
  encodingType: 'rabbit',
  isCompression: false,
  encryptionSecret: process.env.VUE_APP_SECRET,
});

import notifications from './notifications';
import user from './user';
import reader from './reader';
import settings from './settings';

Vue.use(Vuex);

const persistedStateConf = {
  paths: ['user', 'reader'],
  storage: {
    getItem: (key: string) => ls.get(key),
    setItem: (key: string, value: any) => ls.set(key, value),
    removeItem: (key: string) => ls.remove(key),
  },
};

export default new Vuex.Store({
  modules: { notifications, user, reader, settings },
  plugins: [createPersistedState(persistedStateConf)],
});
