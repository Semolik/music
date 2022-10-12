import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'
import { plugin, defaultConfig } from '@formkit/vue'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification";
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'

import './assets/styles/base.scss'
import '@formkit/themes/genesis'
import "vue-toastification/dist/index.css";

const app = createApp(App)
app.config.unwrapInjectedRef = true


app.use(createPinia())
app.use(router);
app.use(autoAnimatePlugin);
app.use(plugin, defaultConfig);
app.use(Toast);

app.mount('#app')

const { getMe } = useAuthStore();
const { initTheme } = useThemeStore();

getMe()
initTheme();