import { defineStore } from 'pinia';
import { HTTP } from '../http-common.vue';
import handleError from '../composables/errors'
import { useStorage } from '@vueuse/core';
export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    message: '',
    loading: false,
    logined: useStorage('logined', false),
  }),
  actions: {
    clearMessage() {
      this.message = '';
    },
    setMessage(error) {
      let message = error?.response?.data?.detail;
      if (message) {
        this.message = message;
      } else {
        this.message = handleError(error).message
      }
    },
    logoutRequest() {
      this.clearMessage();
      HTTP.delete('logout')
        .then((response) => {
          this.logined = false;
        })
        .catch((error) => {
          this.setMessage(error);
        }).finally(() => {
          this.loading = false;
        });
    },
    loginRequest(username, password) {
      this.loading = true;
      this.clearMessage();
      HTTP.post('login', { username: username, password: password })
        .then((response) => {
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
      this.clearMessage();
      HTTP.post('signup', { username: username, password: password, first_name, last_name })
        .then((response) => {
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
          const { detail } = response.data;
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
