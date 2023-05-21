import { OpenAPI } from "@/client";
export default defineNuxtPlugin((nuxtApp) => {
    if (process.server) {
        const cookie = useCookie("access_token_cookie");
        const refreshToken = useCookie("refresh_token_cookie");
        OpenAPI.HEADERS = {
            Cookie: `access_token_cookie=${cookie.value}; refresh_token_cookie=${refreshToken.value}`,
        };
    }

    OpenAPI.BASE =
        process.env.NODE_ENV === "development"
            ? "http://localhost:8000"
            : "http://music.semolik.ru";
    OpenAPI.WITH_CREDENTIALS = true;
});
