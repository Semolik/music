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
    loginRequest(username, password) {
      this.loading = true;
      this.message = '';
      var form = new FormData();
      form.append('username', username);
      form.append('password', password);
      let options = {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded" },
        data: form,
        url: 'token'
      };
      HTTP(options)
        .then((response) => {
          const { access_token, detail } = response.data;
          if (access_token) {
            this.token = access_token;
          } else {
            this.message = detail;
          }
        })
        .catch((error) => {
          this.message = handleError(error)
        }).finally(() => {
          this.loading = false;
        });
    }
  }
});
