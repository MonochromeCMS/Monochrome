import Base from "./Base";
import type {ApiResponse, Pagination} from "./Base";
import type {AxiosRequestConfig} from "axios";

export interface IUser {
  username: string;
  email?: string;
}

export interface UserSchema extends IUser {
  password: string;
}

export interface UserResponse extends IUser {
  id: string;
}

export type UsersResponse = Pagination<UserResponse>;

export default class User extends Base {
  public static readonly prefix: string = "/api/user";

  public static async get_all(auth: AxiosRequestConfig, limit: number = 10, offset: number = 0, delay: boolean = false) {
    const url = `?limit=${limit}&offset=${offset}`;
    const response = await User._get(url, auth, delay);

    const result: ApiResponse<UsersResponse> = User._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = "Please log in again";
      break;
      case 422:
        result.error = "The data provided is not valid";
      break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async me(auth: AxiosRequestConfig) {
    const response = await User._get("/me", auth);

    const result: ApiResponse<UserResponse> = User._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = "Please log in again";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async get(userId: string, auth: AxiosRequestConfig) {
    const response = await User._get(`/${userId}`, auth);

    const result: ApiResponse<UserResponse> = User._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "User not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async edit(userId: string, data: UserSchema, auth: AxiosRequestConfig) {
    const response = await User._put(`/${userId}`, data, auth);

    const result: ApiResponse<UserResponse> = User._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 400:
        result.error = "Username/email already in use";
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "User not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async delete(userId: string, auth: AxiosRequestConfig) {
    const response = await User._delete(`/${userId}`, auth);

    const result: ApiResponse<string> = User._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 400:
        result.error = "You can't delete your own user";
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "User not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async create(data: UserSchema, auth: AxiosRequestConfig) {
    const response = await User._post("", data, auth);

    const result: ApiResponse<UserResponse> = User._apiResponse(response.status);

    switch (response.status) {
      case 201:
        result.data = response.data;
        break;
      case 400:
        result.error = "Username/email already in use";
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }
}