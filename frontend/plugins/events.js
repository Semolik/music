import { useEventBus } from "@vueuse/core";
export default defineNuxtPlugin((nuxtApp) => {
    const goToLoginBus = useEventBus("go-to-login");
    const modalStateBus = useEventBus("modal-state");
    const router = useRouter();
    const unsubscribeLoginBus = goToLoginBus.on(() => {
        modalStateBus.emit(false);
        router.push("/login");
    });
    onBeforeUnmount(() => {
        unsubscribeLoginBus();
    });
});
