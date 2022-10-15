import { createRouter, createWebHistory } from 'vue-router'
import { Role } from '../helpers/roles.js';
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
        {
          path: 'update-status',
          name: 'Изменение статуса аккаунта',
          meta: { requireAuth: true, roles: [Role.User] },
          component: () => import('../components/PersonalАccountChangeStatatus.vue'),
          children: [
            {
              path: 'history',
              name: 'История запросов',
              component: () => import('../components/PersonalAccountChangeStatusHistory.vue'),
            }
          ]
        },
        {
          path: 'update-status-requests',
          name: 'Запросы на изменение статуса',
          meta: { requireAuth: true, roles: [Role.Admin] },
          component: () => import('../components/PersonalАccountChangeStatatusRequests.vue'),
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

  let flag = sessionStorage.getItem('logined');
  let role = sessionStorage.getItem('user-role');
  if (to.meta.requireAuth == true) {
    if (!flag || flag === 'false') {
      next({
        path: '/login'
      })
    } else {
      let roles = to.meta.roles;
      if (roles) {
        if (!role || roles.indexOf(role) < 0) {
          next({
            path: '/login'
          })
        } else {
          return next();
        }
      } else {
        return next();
      }
    }
  } else {
    return next();
  }
});
export default router
