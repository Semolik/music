import { useAuthStore } from "@/stores/auth";

export default defineNuxtPlugin((nuxtApp) => {
    const authStore = useAuthStore();
    authStore.init();
});
