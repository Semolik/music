import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useThemeStore = defineStore({
  id: 'theme',
  state: () => ({
    themeName: useStorage('theme', ''),
  }),
  actions: {
    initTheme() {
      this.setTheme(this.themeName);
      this.StartTrackingThemeChange();
    },
    setTheme(name) {
      if (name) {
        this.setThemeName(name);
      } else {
        this.setThemeName(this.isDark().matches ? 'dark' : 'light');
      }
    },
    toggleTheme() {
      if (this.themeName === 'dark'){
        this.setTheme('light');
      } else {
        this.setTheme('dark');
      }
    },
    setThemeName(name) {
      this.themeName = name;
      document.firstElementChild.setAttribute('data-theme', name);
    },
    isDark() {
      return window.matchMedia('(prefers-color-scheme: dark)');
    },
    StartTrackingThemeChange() {
      this.isDark()
        .addEventListener('change', ({ matches: isDark }) => {
          this.setThemeName(isDark ? 'dark' : 'light');
        })
    }
  }
});
