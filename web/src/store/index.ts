import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

import user from "./user";
import reader from "./reader";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { user, reader },
  plugins: [createPersistedState()],
});
