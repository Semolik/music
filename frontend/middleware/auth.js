export default defineNuxtRouteMiddleware(async (context) => {
    return await useAuthMiddleware(context);
});
