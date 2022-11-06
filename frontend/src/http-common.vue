<script>
import axios from "axios";
import router from './router'

const HTTP = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true
});
HTTP.interceptors.response.use(
  (response) => response,
  (error_1) => {

    if (localStorage.getItem('logined') === 'false' || error_1?.response?.data?.detail !== "Signature has expired") {
      return Promise.reject(error_1);
    }
    axios.post(HTTP.defaults.baseURL + 'refresh', { withCredentials: true })
      .then((res) => {
        const config = error_1.config;
        return new Promise((resolve, reject) => {
          axios
            .request(config)
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              router.push('/login');
              reject(error_1);
            });
        });
      })
      .catch((error_2) => {
        router.push('/login')
        return Promise.reject(error_2);
      });
  });
export { HTTP };
</script>
