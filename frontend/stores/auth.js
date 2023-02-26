import { defineStore } from "pinia";
import { Service } from "@/client";
import { Role } from "@/helpers/roles";

export const useAuthStore = defineStore({
    id: "auth",
    state: () => ({
        message: "",
        logined: false,
        userData: null,
    }),
    getters: {
        fullName() {
            let name = [this.userData.first_name, this.userData.last_name].join(
                " "
            );
            if (name.trim() === "") {
                name = this.userData.username;
            }
            return name;
        },
        isAdmin() {
            return this.userData?.type === Role.Admin;
        },
        isUser() {
            return this.userData?.type === Role.User;
        },
        isMusician() {
            return this.userData?.type === Role.Musician;
        },
        isRadioStation() {
            return this.userData?.type === Role.RadioStation;
        },
    },
    actions: {
        setUserData(data) {
            if (data) {
                this.userData = data;
            }
        },
        logout() {
            this.logined = false;
            this.userData = null;
        },
        async refresh() {
            try {
                await Service.refreshApiV1AuthRefreshPost();
            } catch (error) {
                this.logout();
            }
        },
        async logoutRequest() {
            try {
                await Service.logoutApiV1AuthLogoutDelete();
            } catch (error) {}

            this.logout();
        },
        async loginRequest(username, password) {
            this.logined = false;

            const userData = await Service.loginApiV1AuthLoginPost({
                username: username,
                password: password,
            });
            this.userData = userData;
            this.logined = true;
        },
        async registerRequest(username, password, first_name, last_name) {
            this.logined = false;
            const userData = await Service.createUserSignupApiV1AuthSignupPost({
                username: username,
                password: password,
                first_name,
                last_name,
            });
            this.userData = userData;
            this.logined = true;
        },
        init() {
            this.refresh();
            setInterval(() => {
                if (this.logined) {
                    this.refresh();
                }
            }, 1000 * 60 * 5);
        },
    },
});
