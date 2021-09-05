import Base from "./Base";
import type {ApiResponse, Pagination} from "./Base";
import type {ChapterResponse} from "./Chapter";
import type {AxiosRequestConfig} from "axios";

export type Status = "ongoing" | "completed" | "hiatus" | "cancelled";

export interface MangaSchema {
  title: string;
  description: string;
  author: string;
  artist: string;
  year?: number;
  status: Status;
}

export interface MangaResponse extends MangaSchema {
  id: string;
  verson: number;
  createTime: Date;
}

type MangaSearchResponse = Pagination<MangaResponse>;

export default class Manga extends Base {
  public static readonly prefix: string = "/api/manga";

  public static async search(title: string | null = null, limit: number = 10, offset: number = 0, delay: boolean = false) {
    let url = `?limit=${limit}&offset=${offset}`;

    if (title) {
      url += `?&title=${title}`;
    }

    const response = await Manga._get(url, {}, delay);

    const result: ApiResponse<MangaSearchResponse> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async create(data: MangaSchema, auth: AxiosRequestConfig) {
    const response = await Manga._post("", data, auth);

    const result: ApiResponse<MangaResponse> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 201:
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

  public static async get(mangaId: string, delay: boolean = false) {
    const response = await Manga._get(`/${mangaId}`, {}, delay);

    const result: ApiResponse<MangaResponse> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 404:
        result.error = "Manga not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async edit(mangaId: string, data: MangaSchema, auth: AxiosRequestConfig) {
    const response = await Manga._put(`/${mangaId}`, data, auth);

    const result: ApiResponse<MangaResponse> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "Manga not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async delete(mangaId: string, auth: AxiosRequestConfig) {
    const response = await Manga._delete(`/${mangaId}`, auth);

    const result: ApiResponse<string> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = "OK";
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "Manga not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async chapters(mangaId: string, delay: boolean = false) {
    const url = `/${mangaId}/chapters`;
    const response = await Manga._get(url, {}, delay);

    const result: ApiResponse<ChapterResponse[]> = Manga._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 404:
        result.error = "Manga not found";
        break;
      case 422:
        result.error = "The data provided is not valid";
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async setCover(mangaId: string, cover: File, auth: AxiosRequestConfig) {
    const url = `/${mangaId}/cover`;
    const form = new FormData();
    form.append("payload", cover);

    const response = await Manga._put(url, form, auth, "multipart/form-data");

    const result = Manga._apiResponse(response.status);
    
    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 400:
        result.error = "The cover provided is not an image";
        break;
      case 401:
        result.error = "Please log in again";
        break;
      case 404:
        result.error = "Manga not found";
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
