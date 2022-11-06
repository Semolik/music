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
      component: () => import('../views/PersonalAccountView.vue'),
      children: [
        {
          path: '',
          name: 'Личный кабинет',
          component: () => import('../components/PersonalAccountProfile.vue'),
        },
        {
          path: 'public',
          name: 'Публичный профиль',
          component: () => import('../components/PersonalAccountPublicProfile.vue'),
        },
        {
          path: 'music',
          name: 'Моя музыка',
          component: () => import('../components/PersonalAccountMusic.vue'),
        },
        {
          path: 'my-music',
          component: () => import('../components/PersonalAccountMusicianCabinet.vue'),
          children: [
            {
              path: '',
              name: 'Кабинет музыканта',
              component: () => import('../components/PersonalAccountMusicianCabinetMain.vue'),
            },
            {
              path: 'upload',
              name: 'Загрузить',
              component: () => import('../components/PersonalAccountMusicianCabinetUpload.vue'),
            },
            {
              path: 'albums',
              name: 'Альбомы',
              component: () => import('../components/PersonalAccountMusicianCabineAlbums.vue'),
            },
            {
              path: 'albums/:id',
              name: 'Альбом',
              component: () => import('../components/PersonalAccountMusicianCabineAlbumsAlbum.vue'),
            }
          ]
        },
        {
          path: 'update-status',
          name: 'Изменение статуса аккаунта',
          meta: { requireAuth: true, roles: [Role.User, Role.Musician, Role.RadioStation] },
          component: () => import('../components/PersonalAccountChangeStatatus.vue'),
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
          component: () => import('../components/PersonalAccountChangeStatatusRequests.vue'),
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
