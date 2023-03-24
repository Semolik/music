import { UserTypeEnum } from "@/client/models/UserTypeEnum";
export default defineNuxtRouteMiddleware(async (context) => {
    return await useAuthMiddleware(context, UserTypeEnum.USER);
});
