import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Главная',
      component: HomeView
    },
    {
      path: '/login',
      name: 'Авторизация',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/lk',
      component: () => import('../views/PersonalАccountView.vue'),
      children: [
        {
          path: '',
          name: 'Личный кабинет',
          component: () => import('../components/PersonalАccountViewProfile.vue'),
        },
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Страница не найдена',
      alias: '/404',
      component: () => import('../components/AppError.vue')
    },
  ]
});
router.beforeEach((to, from, next) => {
  document.title = to.name;
  window.scrollTo(0, 0)
  next();
});
export default router
