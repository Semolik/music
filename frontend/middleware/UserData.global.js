import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware(async (context) => {
    if (process.server) {
        const authStore = useAuthStore();
        await authStore.getUserData();
    }
});
