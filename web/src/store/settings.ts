import type { ActionContext } from "vuex";
import type { AxiosRequestConfig, AxiosResponse } from "axios";
import axios from "axios";

export interface SettingsState {
  title1: string | null;
  title2: string | null;
  about: string | null;
}

const state = (): SettingsState => ({
  title1: null,
  title2: null,
  about: null,
});

const mutations = {
  setSettings(state: SettingsState, payload: SettingsState): void {
    state.about = payload.about;
    state.title1 = payload.title1;
    state.title2 = payload.title2;
  },
};

const getters = {
  settings(state: SettingsState): SettingsState {
    return state
  }
};

const actions = {
  async getSettings({
    state,
    commit,
  }: ActionContext<SettingsState, any>): Promise<AxiosResponse> {
    const url = "/api/settings";

    try {
      const response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
        },
      });
      commit("setSettings", response.data);
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async editSettings(
    { state, rootGetters, commit, dispatch }: ActionContext<SettingsState, any>,
    settings: SettingsState
  ): Promise<AxiosResponse> {
    const url = "/api/settings";

    const config = rootGetters.authConfig;
    config.headers["Content-Type"] = "application/json";

    try {
      const response = await axios.put(url, settings, config);
      dispatch("getSettings").then();
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
};

export default {
  state,
  actions,
  getters,
  mutations,
};
