import type { ApiResponse } from './Base';
import Base from './Base';
import type { AxiosRequestConfig } from 'axios';

export interface SettingsSchema {
  title1?: string;
  title2?: string;
  about?: string;
}

export default class Settings extends Base {
  public static readonly router: string = '/settings';

  public static async get() {
    const response = await Settings._get('', {});

    const result: ApiResponse<SettingsSchema> = Settings._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      default:
        result.error = response.data.detail ?? response.statusText;
    }
    return result;
  }

  public static async edit(data: SettingsSchema, auth: AxiosRequestConfig) {
    const response = await Settings._put('', data, auth);
    const result: ApiResponse<SettingsSchema> = Settings._apiResponse(response.status);

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = 'Please log in again';
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
