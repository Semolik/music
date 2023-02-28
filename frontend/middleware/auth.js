import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
export default defineNuxtRouteMiddleware(async (context) => {
    const authStore = useAuthStore();
    const { logout, refresh } = authStore;
    const { logined } = storeToRefs(authStore);
    if (process.server) {
        const cookie = useCookie("access_token_cookie");
        if (cookie.value) {
            try {
                const request = await axios.post(
                    "http://localhost:8000/api/v1/auth/refresh",
                    {
                        withCredentials: true,
                        headers: {
                            Cookie: `access_token_cookie=${cookie.value}`,
                        },
                    }
                );
                if (request.status === 200) {
                    logined.value = true;
                }
            } catch (error) {}

            if (!logined.value) {
                logout();
                return navigateTo("/login");
            }
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value) {
            return navigateTo("/login");
        }
    }
});
