import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';
import { HTTP } from '../http-common.vue';
import { handleError } from 'vue';
export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    token: useStorage('token', ''),
    message: '',
    loading: false,
  }),
  actions: {
    clearMessage(){
      this.message = '';
    },
    loginRequest(username, password) {
      this.loading = true;
      this.clearMessage();
      HTTP.post('login', { username: username, password: password })
        .then((response) => {
          const { access_token, detail } = response.data;
          if (access_token) {
            this.token = access_token;
          } else {
            this.message = detail;
          }
        })
        .catch((error) => {
          if (error?.response?.status===401){
            this.message = error.response.data.detail;
          }else {
            this.message = handleError(error)
          }
        }).finally(() => {
          this.loading = false;
        });
    }
  }
});
