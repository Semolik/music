import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

export default defineNuxtRouteMiddleware(async (context) => {
    if (process.server) {
        const authStore = useAuthStore();
        const { logout } = authStore;
        const { userData, logined } = storeToRefs(authStore);
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
            } catch (error) {}
        }
        if (!logined.value) {
            logout();
            if (context.path !== "/login") {
                return navigateTo("/login");
            }
        }
    }
});
