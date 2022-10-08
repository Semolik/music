import { defineStore } from 'pinia';
import { HTTP } from '../http-common.vue';
import handleError from '../composables/errors'
import { useSessionStorage } from '@vueuse/core';
import { Role } from '../helpers/roles.js';
export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    message: '',
    loading: false,
    logined: useSessionStorage('logined', false),
    userRole: useSessionStorage('user-role', null),
    userData: null,
  }),
  actions: {
    clearMessage() {
      this.message = '';
    },
    setUserRole() {
      this.userRole = null;
      let user = this.userData;
      Object.values(Role).forEach(role_key => {
        if (user[role_key] === true) {
          this.userRole = role_key;
        }
      });
      if (!this.userRole) {
        this.userRole = Role.User;
      }
    },
    setUserData(data) {
      if (data) {
        this.userData = data;
        this.setUserRole();
      }
    },
    setMessage(error) {
      let message = error?.response?.data?.detail;
      if (message) {
        this.message = message;
      } else {
        this.message = handleError(error).message
      }
    },
    logout() {
      this.logined = false;
      this.userData = null;
      this.userRole = null;
    },
    logoutRequest() {
      this.clearMessage();
      HTTP.delete('logout')
        .then((response) => {
          this.logout();
        })
        .catch((error) => {
          this.setMessage(error);
        }).finally(() => {
          this.loading = false;
        });
    },
    loginRequest(username, password) {
      this.loading = true;
      this.logined = false;
      this.clearMessage();
      HTTP.post('login', { username: username, password: password })
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.setMessage(error);
          this.logined = false;
        }).finally(() => {
          this.loading = false;
        });
    },
    registerRequest(username, password, first_name, last_name) {
      this.loading = true;
      this.logined = false;
      this.clearMessage();
      HTTP.post('signup', { username: username, password: password, first_name, last_name })
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.setMessage(error);
          this.logined = false;
        }).finally(() => {
          this.loading = false;
        });
    },
    getMe() {
      this.loading = true;
      this.clearMessage();
      HTTP.get('me')
        .then((response) => {
          this.userData = response.data;
          this.setUserRole();
          this.logined = true;
        })
        .catch((error) => {
          this.logined = false;
        }).finally(() => {
          this.loading = false;
        });
    }
  }
});
