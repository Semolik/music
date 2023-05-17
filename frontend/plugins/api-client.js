import { OpenAPI } from "@/client";
export default defineNuxtPlugin((nuxtApp) => {
    if (process.server) {
        const cookie = useCookie("access_token_cookie");
        const refreshToken = useCookie("refresh_token_cookie");
        OpenAPI.HEADERS = {
            Cookie: `access_token_cookie=${cookie.value}; refresh_token_cookie=${refreshToken.value}`,
        };
    }
    OpenAPI.BASE = "http://tsoa-voloshin.ru/api";
    OpenAPI.WITH_CREDENTIALS = true;
});
