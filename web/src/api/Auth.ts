import Base, { ApiResponse } from "./Base";

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
}

export default class Auth extends Base {
  public static readonly prefix: string = "/api/auth";

  public static async login(username: string, password: string) {
    const form = new FormData();
    form.append("grant_type", "password");
    form.append("username", username);
    form.append("password", password);
    form.append("scope", "");
    form.append("client_id", "");
    form.append("client_secret", "");

    const response = await Auth._post(
      "/token",
      form,
      {},
      "application/x-www-form-urlencoded"
    );

    const result: ApiResponse<TokenResponse> = Auth._apiResponse(
      response.status
    );

    switch (response.status) {
      case 200:
        result.data = response.data;
        break;
      case 401:
        result.error = "Credentials don't match";
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
