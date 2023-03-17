import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames, navigateTo } from "@typed-router";
export const useAuthMiddleware = async (context, userType) => {
    const authStore = useAuthStore();
    const { logout, refresh } = authStore;
    const { logined, userData } = storeToRefs(authStore);
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
                    logined.value = true;
                }

                if (userType && request.data.type !== userType) {
                    logout();
                    return navigateTo({ name: routesNames.login });
                }
            } catch (error) {}

            if (!logined.value) {
                logout();
                return navigateTo({ name: routesNames.login });
            }
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value) {
            return navigateTo({ name: routesNames.login });
        }
        if (userType && userData.value.type !== userType) {
            return navigateTo({ name: routesNames.login });
        }
    }
};
