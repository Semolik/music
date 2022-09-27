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
      meta: { requireAuth: true },
      component: () => import('../views/PersonalАccountView.vue'),
      children: [
        {
          path: '',
          name: 'Личный кабинет',
          component: () => import('../components/PersonalАccountProfile.vue'),
        },
        {
          path: 'music',
          name: 'Моя музыка',
          component: () => import('../components/PersonalАccountMusic.vue'),
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
  let flag = sessionStorage.getItem('logined')

  if (to.meta.requireAuth == true) {// Маршрут, требующий разрешения на вход
    if (!flag || flag === 'false') {// Невозможно получить данные для входа
      next({
        path: '/login'
      })
    } else {// Получите информацию для входа и перейдите к следующему шагу
      return next();
    }
  } else {// Непосредственно перейти к следующему шагу без разрешения на вход
    return next();
  }
});
export default router
