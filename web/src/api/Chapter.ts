import type { ApiResponse, Pagination } from './Base';
import Base from './Base';
import type { AxiosRequestConfig } from 'axios';
import type { MangaResponse } from '@/api/Manga';

export interface ChapterSchema {
  name: string;
  webtoon: boolean;
  volume?: number;
  number: number;
  scanGroup: string;
}

export interface ChapterResponse extends ChapterSchema {
  id: string;
  version: number;
  mangaId: string;
  length: number;
  uploadTime: string;
}

export interface DetailedChapterResponse extends ChapterResponse {
  manga: MangaResponse;
}

type LatestChaptersResponse = Pagination<DetailedChapterResponse>;

export default class Chapter extends Base {
  public static readonly router: string = '/chapter';

  public static async latest(limit = 10, offset = 0, delay = false) {
    const url = `?limit=${limit}&offset=${offset}`;

    const response = await this._get(url, {}, delay);

    const result: ApiResponse<LatestChaptersResponse> = this._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 422:
        result.error = 'The data provided is not valid';
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async get(chapterId: string, delay = false) {
    const response = await this._get(`/${chapterId}`, {}, delay);

    const result: ApiResponse<DetailedChapterResponse> = this._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 404:
        result.error = 'Chapter not found';
        break;
      case 422:
        result.error = 'The data provided is not valid';
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async edit(chapterId: string, data: ChapterSchema, auth: AxiosRequestConfig) {
    const response = await this._put(`/${chapterId}`, data, auth);

    const result: ApiResponse<ChapterResponse> = this._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = 'Please log in again';
        break;
      case 404:
        result.error = 'Chapter not found';
        break;
      case 422:
        result.error = 'The data provided is not valid';
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async delete(chapterId: string, auth: AxiosRequestConfig) {
    const response = await this._delete(`/${chapterId}`, auth);

    const result: ApiResponse<string> = this._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = 'OK';
        break;
      case 401:
        result.error = 'Please log in again';
        break;
      case 404:
        result.error = 'Chapter not found';
        break;
      case 422:
        result.error = 'The data provided is not valid';
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }
}
