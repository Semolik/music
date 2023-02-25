import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

export default defineNuxtRouteMiddleware(async (context) => {
    if (process.server) {
        const authStore = useAuthStore();
        const { userData, logined } = storeToRefs(authStore);
        const cookie = useCookie("access_token_cookie");
        if (cookie.value) {
            const request = await axios.get(
                "http://localhost:8000/api/v1/users/me",
                {
                    withCredentials: true,
                    headers: {
                        Cookie: `access_token_cookie=${cookie.value}`,
                    },
                    validateStatus: (status) => status < 500,
                }
            );
            if (request.status === 200) {
                userData.value = request.data;
                logined.value = true;
            }
        }
        if (!logined.value) {
            authStore.logout();
        }
    }
});
