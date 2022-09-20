import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'
import { SetupCalendar } from 'v-calendar';

import App from './App.vue'
import router from './router'

import './assets/styles/base.scss'

const app = createApp(App)
app.config.unwrapInjectedRef = true


app.use(createPinia())
app.use(router)
app.use(SetupCalendar, {})

app.mount('#app')

const { getMe } = useAuthStore();
const { initTheme } = useThemeStore();

getMe()
initTheme();