import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
export default defineNuxtRouteMiddleware(async (context) => {
    const authStore = useAuthStore();
    const { logout, refresh } = authStore;
    const { userData, logined } = storeToRefs(authStore);
    if (process.server) {
        const cookie = useCookie("access_token_cookie");
        if (cookie.value) {
            try {
                const request = await axios.get(
                    "http://localhost:8000/api/v1/users/me",
                    {
                        withCredentials: true,
                        headers: {
                            Cookie: `access_token_cookie=${cookie.value}`,
                        },
                    }
                );
                if (request.status === 200) {
                    userData.value = request.data;
                    logined.value = true;
                    this.setUserRole();
                }
            } finally {
                if (!logined.value) {
                    logout();
                    return navigateTo("/login");
                }
            }
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value) {
            return navigateTo("/login", { replace: true });
        }
    }
});
