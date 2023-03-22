import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames, navigateTo } from "@typed-router";
export const useAuthMiddleware = async (context, userType) => {
    const authStore = useAuthStore();
    const { logout, refresh } = authStore;
    const { logined, userData } = storeToRefs(authStore);
    if (process.server) {
        await authStore.getUserData();
        if ((userType && userData?.type !== userType) || !logined.value) {
            logout();
            return navigateTo({ name: routesNames.login });
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value || (userType && userData.value.type !== userType)) {
            return navigateTo({ name: routesNames.login });
        }
    }
};
