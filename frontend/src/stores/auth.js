import { defineStore } from "pinia";
import { HTTP } from "../http-common.vue";
import handleError from "../composables/errors";
import { useSessionStorage } from "@vueuse/core";
import { Role } from "../helpers/roles.js";
import router from "../router";
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
      this.message = handleError(error).message;
    },
    logout() {
      this.logined = false;
      this.userData = null;
      this.userRole = null;
    },
    refresh() {
      HTTP.post("refresh", { withCredentials: true })
        .then((response) => {})
        .catch((error) => {
          router.push("/login");
        });
    },
    logoutRequest() {
      this.clearMessage();
      HTTP.delete("logout")
        .then((response) => {
          this.logout();
        })
        .catch((error) => {
          this.setMessage(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    loginRequest(username, password) {
      this.loading = true;
      this.logined = false;
      this.clearMessage();
      HTTP.post("login", { username: username, password: password })
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.setMessage(error);
          this.logined = false;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    registerRequest(username, password, first_name, last_name) {
      this.loading = true;
      this.logined = false;
      this.clearMessage();
      HTTP.post("signup", {
        username: username,
        password: password,
        first_name,
        last_name,
      })
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.setMessage(error);
          this.logined = false;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getMe() {
      this.loading = true;
      this.clearMessage();
      HTTP.get("me")
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.logined = false;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
});
