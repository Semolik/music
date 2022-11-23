import { createRouter, createWebHistory } from 'vue-router'
import { Role } from '../helpers/roles.js';
import HomeView from '../views/HomeView.vue';
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
      component: () => import('../views/SettingsView.vue'),
      children: [
        {
          path: '',
          name: 'Личный кабинет',
          component: () => import('../components/Settings/Profile.vue'),
        },
        {
          path: 'public',
          name: 'Публичный профиль',
          meta: { requireAuth: true, roles: [Role.Musician, Role.RadioStation] },
          component: () => import('../components/Settings/PublicProfile.vue'),
        },
        {
          path: 'music',
          name: 'Моя музыка',
          component: () => import('../components/Settings/Music/index.vue'),
        },
        {
          path: 'my-music',
          component: () => import('../components/Settings/Musician/Cabinet/index.vue'),
          meta: { requireAuth: true, roles: [Role.Musician] },
          children: [
            {
              path: '',
              name: 'Кабинет музыканта',
              meta: { requireAuth: true, roles: [Role.Musician] },
              component: () => import('../components/Settings/Musician/Cabinet/Main.vue'),
            },
            {
              path: 'upload',
              name: 'Загрузить',
              meta: { requireAuth: true, roles: [Role.Musician] },
              component: () => import('../components/Settings/Musician/Cabinet/Upload/index.vue'),
            },
            {
              path: 'albums',
              name: 'Альбомы',
              meta: { requireAuth: true, roles: [Role.Musician] },
              component: () => import('../components/Settings/Musician/Albums/index.vue'),
            },
            {
              path: 'albums/:id',
              name: 'Альбом',
              props: true,
              meta: { requireAuth: true, roles: [Role.Musician] },
              component: () =>  import('../components/Settings/Musician/Album.vue'),
            }
          ]
        },
        {
          path: 'update-status',
          name: 'Изменение статуса аккаунта',
          meta: { requireAuth: true, roles: [Role.User, Role.Musician, Role.RadioStation] },
          component: () => import('../components/Settings/ChangeStatatus/index.vue'),
          children: [
            {
              path: 'history',
              name: 'История запросов',
              component: () => import('../components/Settings/ChangeStatatus/History/index.vue'),
            }
          ]
        },
        {
          path: 'update-status-requests',
          name: 'Запросы на изменение статуса',
          meta: { requireAuth: true, roles: [Role.Admin] },
          component: () => import('../components/Settings/ChangeStatatus/Requests.vue'),
        },
        {
          path: 'edit-musician-section',
          name: 'Музыкальный раздел',
          meta: { requireAuth: true, roles: [Role.Admin] },
          component: () => import('../components/Settings/AdminEditMusicians/Section.vue'),
        },
        {
          path: 'edit-musician-section/genres',
          name: 'Жанры',
          meta: { requireAuth: true, roles: [Role.Admin] },
          component: () => import('../components/Settings/AdminEditMusicians/Genres.vue'),
        },
        {
          path: 'edit-musician-section/genres/:id',
          name: 'Жанр',
          meta: { requireAuth: true, roles: [Role.Admin] },
          props: true,
          component: () => import('../components/Settings/AdminEditMusicians/Genre.vue'),
        },
        {
          path: 'edit-musician-section/genres/add',
          name: 'Добавить жанр',
          meta: { requireAuth: true, roles: [Role.Admin] },
          props: { add: true },
          component: () => import('../components/Settings/AdminEditMusicians/Genre.vue'),
        }
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
