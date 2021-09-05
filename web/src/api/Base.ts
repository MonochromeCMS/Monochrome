import axios, {AxiosResponse} from "axios";
import type { AxiosRequestConfig } from "axios";

export interface Pagination<T> {
  offset: number;
  limit: number;
  total: number;
  results: T[];
}

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

export default class Base {
  public static readonly prefix: string = "/api";

  public static _delay() {
    return new Promise((resolve) => {
      setTimeout(() => resolve("done!"), 450);
    });
  }

  public static async _get(url: string, config: AxiosRequestConfig, delay: boolean = false): Promise<AxiosResponse> {
    try {
      const response = await axios.get(this.prefix + url, config);
      if (delay) {
        await Base._delay();
      }
      return response;
    } catch (error) {
      return error?.response;
    }
  }

  public static async _delete(url: string, config: AxiosRequestConfig): Promise<AxiosResponse> {
    try {
      return await axios.delete(this.prefix + url, config);
    } catch (error) {
      return error?.response;
    }
  }

  public static async _post(url: string, data: any, config: AxiosRequestConfig, contentType: string = ""): Promise<AxiosResponse> {
    const settings = { headers: {}, ...config };
    settings.headers["Content-Type"] = contentType || "application/json";

    try {
      return await axios.post(this.prefix + url, data, settings);
    } catch (error) {
      return error?.response;
    }
  }

  public static async _put(url: string, data: any, config: AxiosRequestConfig, contentType: string = ""): Promise<AxiosResponse> {
    const settings = { ...config };
    settings.headers["Content-Type"] = contentType || "application/json";

    try {
      return await axios.put(this.prefix + url, data, settings);
    } catch (error) {
      return error?.response;
    }
  }
  
  public static _apiResponse(status: number): ApiResponse<any> {
    return {
      data: null,
      error: null,
      status,
    };
  }
}
