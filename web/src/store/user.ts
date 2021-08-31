import type { ActionContext } from "vuex";
import type { AxiosRequestConfig, AxiosResponse } from "axios";
import axios from "axios";
import qs from "qs";

interface TokenPayload {
  accessToken: string;
  tokenType: string;
}

interface User {
  token: string;
  username?: string;
  email?: string;
  id?: string;
}

export interface UserState {
  user: User;
  users: User[];
  endpoints: Record<string, string>;
}

export interface UserLogin {
  username: string;
  password: string;
}

type UserEdit = [string, User];

const state = (): UserState => ({
  user: {
    token: "",
  },
  users: [],
  endpoints: {
    userData: "/api/user/me",
    login: "/api/token",
    users: "/api/user",
  },
});

const mutations = {
  setToken(state: UserState, payload: TokenPayload): void {
    state.user.token = payload.accessToken;
  },
  logout(state: UserState): void {
    state.user = {
      token: "",
    };
    state.users = [];
  },
  updateUser(state: UserState, payload: User): void {
    Object.assign(state.user, payload);
  },
  updateUsers(state: UserState, payload: User[]): void {
    state.users = payload;
  },
};

const getters = {
  userId(state: UserState): string | null {
    return state.user.id ?? null;
  },
  isConnected(state: UserState): boolean {
    return !!state.user.token;
  },
  authStr(state: UserState): string {
    return "Bearer ".concat(state.user.token);
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
    { state, commit, dispatch }: ActionContext<UserState, any>,
    form: UserLogin
  ): Promise<AxiosResponse> {
    const url = state.endpoints.login;

    try {
      const response = await axios(url, {
        method: "POST",
        headers: {
          Accept: "*/*",
          "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
        data: qs.stringify(form),
      });
      commit("setToken", response.data);
      dispatch("getUserData").then();
      return response;
    } catch (e) {
      console.error(e);
      return e.response;
    }
  },
  async getUserData({
    state,
    commit,
  }: ActionContext<UserState, any>): Promise<AxiosResponse> {
    const url = state.endpoints.userData;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      const response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        withCredentials: true,
      });
      commit("updateUser", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async getUsers({
    state,
    commit,
  }: ActionContext<UserState, any>): Promise<AxiosResponse> {
    const url = state.endpoints.users;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      const response = await axios(url, {
        method: "GET",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        withCredentials: true,
      });
      commit("updateUsers", response.data);
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async deleteUser(
    { state, commit, dispatch }: ActionContext<UserState, any>,
    id: string
  ): Promise<AxiosResponse | boolean> {
    if (state.user.id === id) return false;

    const url = `${state.endpoints.users}/${id}`;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      const response = await axios(url, {
        method: "DELETE",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
        },
        withCredentials: true,
      });
      dispatch("getUsers").then();
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async editUser(
    { state, commit, dispatch }: ActionContext<UserState, any>,
    [id, data]: UserEdit
  ): Promise<AxiosResponse> {
    const url = `${state.endpoints.users}/${id}`;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      const response = await axios(url, {
        method: "PUT",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        withCredentials: true,
        data: data,
      });
      if (state.user.id === id) {
        commit("logout");
      } else {
        dispatch("getUsers").then();
      }
      return response;
    } catch (e) {
      console.error(e);
      if (e.response.status === 401) {
        commit("logout");
      }
      return e.response;
    }
  },
  async createUser(
    { state, commit, dispatch }: ActionContext<UserState, any>,
    data: Record<string, any>
  ): Promise<AxiosResponse> {
    const url = state.endpoints.users;

    const AuthStr = "Bearer ".concat(state.user.token);

    try {
      const response = await axios(url, {
        method: "POST",
        headers: {
          Accept: "*/*",
          Authorization: AuthStr,
          "Content-Type": "application/json",
        },
        withCredentials: true,
        data: data,
      });
      dispatch("getUsers").then();
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
