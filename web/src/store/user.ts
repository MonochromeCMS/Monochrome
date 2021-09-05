import type { ActionContext } from "vuex";
import type { AxiosRequestConfig } from "axios";

import Auth from "@/api/Auth";
import type { TokenResponse } from "@/api/Auth";
import User from "@/api/User";
import type { UserResponse } from "@/api/User";
import { ApiResponse } from "@/api/Base";

interface IUser {
  token: string;
  username?: string;
  email?: string;
  id?: string;
}

export interface UserState {
  user: IUser;
}

export interface UserLogin {
  username: string;
  password: string;
}

const state = (): UserState => ({
  user: {
    token: "",
  },
});

const mutations = {
  setToken(state: UserState, payload: TokenResponse): void {
    state.user.token = payload.access_token;
  },
  logout(state: UserState): void {
    state.user = {
      token: "",
    };
  },
  updateUser(state: UserState, payload: UserResponse): void {
    Object.assign(state.user, payload);
  },
};

const getters = {
  userId(state: UserState): string | null {
    return state.user.id ?? null;
  },
  isConnected(state: UserState): boolean {
    return !!state.user.token;
  },
  authConfig(state: UserState): AxiosRequestConfig {
    return {
      headers: {
        Accept: "*/*",
        Authorization: "Bearer ".concat(state.user.token),
      },
      withCredentials: true,
    };
  },
};

const actions = {
  async login(
    { commit, dispatch }: ActionContext<UserState, any>,
    { username, password }: UserLogin
  ): Promise<ApiResponse<TokenResponse>> {
    const response = await Auth.login(username, password);

    if (response.data) {
      commit("setToken", response.data);
      dispatch("getUserData").then();
    }
    return response;
  },
  async getUserData({
    getters,
    commit,
  }: ActionContext<UserState, any>): Promise<ApiResponse<UserResponse>> {
    const response = await User.me(getters.authConfig);

    if (response.data) {
      commit("updateUser", response.data);
    } else if (response.status === 401) {
      commit("logout");
    }
    return response;
  },
};

export default {
  state,
  actions,
  getters,
  mutations,
};
