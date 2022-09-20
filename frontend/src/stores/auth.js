import { defineStore } from 'pinia';
import { HTTP } from '../http-common.vue';
import { handleError } from 'vue';
export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    message: '',
    loading: false,
    logined: false,
  }),
  actions: {
    clearMessage() {
      this.message = '';
    },
    loginRequest(username, password) {
      this.loading = true;
      this.clearMessage();
      HTTP.post('login', { username: username, password: password })
        .then((response) => {
          this.logined = true;
        })
        .catch((error) => {
          if (error?.response?.status === 401) {
            this.message = error.response.data.detail;
          } else {
            this.message = handleError(error)
          }
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
