<script>
import axios from "axios";
import { useStorage } from '@vueuse/core';
import { useAuthStore } from './stores/auth';

const HTTP = axios.create({
  baseURL: 'http://localhost:3000/api/v1/',
  withCredentials: true
});
HTTP.interceptors.response.use(
  (response) => response,
  (error) => {
    if (localStorage.getItem('logined') === 'false' && error?.response?.data?.detail !== "Signature has expired") {
      return Promise.reject(error);
    }
    axios.post(HTTP.defaults.baseURL + 'refresh')
      .then((res) => {
        const config = error.config;
        return new Promise((resolve, reject) => {
          axios
            .request(config)
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              reject(error);
            });
        });
      })
      .catch((error) => {
        console.log('Выход из аккаунта')
        // поставить выход из аккаунта
        return Promise.reject(error);
      });
  });
export { HTTP };
</script>
