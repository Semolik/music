import { defineStore } from "pinia";
import { Service } from "@/client";
import { HandleAxiosError } from "@/composables/errors";
import { useSessionStorage } from "@vueuse/core";
import { Role } from "@/helpers/roles";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore({
    id: "auth",
    state: () => ({
        message: "",
        loading: false,
        logined: useSessionStorage("logined", false),
        userRole: useSessionStorage("user-role", null),
        userData: null,
        isAdmin: false,
        isUser: false,
        isMusician: false,
        isRadioStation: false,
    }),
    actions: {
        clearMessage() {
            this.message = "";
        },
        setUserRole() {
            this.userRole = null;
            let user = this.userData;

            this.isAdmin = false;
            this.isUser = false;
            this.isRadioStation = false;
            this.isMusician = false;
            switch (user.type) {
                case Role.Admin:
                    this.userRole = Role.Admin;
                    this.isAdmin = true;
                    break;
                case Role.User:
                    this.userRole = Role.User;
                    this.isUser = true;
                    break;
                case Role.Musician:
                    this.userRole = Role.Musician;
                    this.isMusician = true;
                    break;
                case Role.RadioStation:
                    this.userRole = Role.RadioStation;
                    this.isRadioStation = true;
                    break;
                default:
                    this.userRole = Role.User;
                    this.isUser = true;
                    break;
            }
        },
        setUserData(data) {
            if (data) {
                this.userData = data;
                this.setUserRole();
            }
        },
        setMessage(error) {
            this.message = HandleAxiosError(error).message;
        },
        logout() {
            this.logined = false;
            this.userData = null;
            this.userRole = null;
        },
        async refresh() {
            try {
                await Service.refreshApiV1AuthRefreshPost();
            } catch (error) {
                this.logout();
            }
        },
        async logoutRequest() {
            this.clearMessage();
            try {
                await Service.logoutApiV1AuthLogoutDelete();
            } catch (error) {}

            this.logout();
        },
        async loginRequest(username, password) {
            this.loading = true;
            this.logined = false;
            this.clearMessage();
            const userData = await Service.loginApiV1AuthLoginPost({
                username: username,
                password: password,
            });
            this.userData = userData;
            this.setUserRole();
            this.logined = true;
            this.loading = false;
        },
        async registerRequest(username, password, first_name, last_name) {
            this.loading = true;
            this.logined = false;
            const userData = await Service.createUserSignupApiV1AuthSignupPost({
                username: username,
                password: password,
                first_name,
                last_name,
            });
            this.userData = userData;
            this.setUserRole();
            this.logined = true;
            this.loading = false;
        },
        getMe() {
            this.loading = true;
            this.clearMessage();
            const userData = Service.getUserInfoApiV1UsersMeGet();
            this.userData = userData;
            this.setUserRole();
            this.logined = true;
            this.loading = false;
        },
    },
});
