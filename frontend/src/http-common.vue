<script>
import axios from "axios";

const HTTP = axios.create({
  baseURL: 'http://192.168.50.106:3000/api/v1/',
  withCredentials: true
});
HTTP.interceptors.response.use(
  (response) => response,
  (error) => {
    if (localStorage.getItem('logined') === 'false' || error?.response?.data?.detail !== "Signature has expired") {
      return Promise.reject(error);
    }
    axios.post(HTTP.defaults.baseURL + 'refresh', { withCredentials: true })
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
