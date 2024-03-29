export default defineNuxtConfig({
    modules: [
        "nuxt-icon",
        "@element-plus/nuxt",
        "@nuxtjs/tailwindcss",
        "@nuxtjs/google-fonts",
        "@pinia/nuxt",
        "@vueuse/nuxt",
        "nuxt-typed-router",
        "nuxt-viewport",
        "@nuxt/devtools",
        "nuxt-swiper",
    ],
    devtools: {
        enabled: true,
        vscode: {},
    },
    app: {
        head: {
            htmlAttrs: {
                lang: "ru",
                class: "dark",
            },
            link: [{ rel: "icon", type: "image/png", href: "/favicon.png" }],
        },
    },
    viewport: {
        breakpoints: {
            xs: 360,
            sm: 576,
            md: 768,
            lg: 992,
            xl: 1200,
        },
    },
    nuxtTypedRouter: {
        strict: true,
    },
    googleFonts: {
        families: {
            "Open+Sans": true,
        },
        download: true,
    },
    plugins: [
        { src: "~/plugins/autoAnimatePlugin.js", mode: `client` },
        { src: "~/plugins/refreshToken.js", mode: `client` },
        { src: "~/plugins/events.js", mode: `client` },
        { src: "~/plugins/vue-toastification.js", mode: `client` },
        { src: "~/plugins/api-client.js" },
    ],
    nitro: {
        devProxy: {
            "/api": {
                target: "http://localhost:8000/api",
                changeOrigin: true,
                prependPath: true,
                cookieDomainRewrite: false,
            },
            "/api/docs": {
                target: "http://localhost:8000/docs",
                changeOrigin: true,
                prependPath: true,
            },
        },
    },
    css: ["@/assets/styles/global.scss"],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: [
                        '@use "@/assets/styles/_colors.scss" as *;',
                        '@use "@/assets/styles/helpers.scss" as *;',
                        '@use "@/assets/styles/breakpoints.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
    runtimeConfig: {
        public: {
            AuthBusKey: "auth",
            MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH: Number(
                process.env.VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH
            ),
            MAX_PUBLIC_PROFILE_NAME_LENGTH: Number(
                process.env.VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH
            ),
            MAX_FIRSTNAME_LENGTH: Number(process.env.VITE_MAX_FIRSTNAME_LENGTH),
            MAX_LASTNAME_LENGTH: Number(process.env.VITE_MAX_LASTNAME_LENGTH),
            MAX_PASSWORD_LENGTH: Number(process.env.VITE_MAX_PASSWORD_LENGTH),
            MIN_PASSWORD_LENGTH: Number(process.env.VITE_MIN_PASSWORD_LENGTH),
            MIN_LOGIN_LENGTH: Number(process.env.VITE_MIN_LOGIN_LENGTH),
            MAX_LOGIN_LENGTH: Number(process.env.VITE_MAX_LOGIN_LENGTH),
            LOGIN_REGEX: process.env.VITE_LOGIN_REGEX,
            MAX_TRACK_NAME_LENGTH: Number(
                process.env.VITE_MAX_TRACK_NAME_LENGTH
            ),
            MIN_TRACK_NAME_LENGTH: Number(
                process.env.VITE_MIN_TRACK_NAME_LENGTH
            ),
            MAX_TRACK_FEAT_LENGTH: Number(
                process.env.VITE_MAX_TRACK_FEAT_LENGTH
            ),
            MAX_ALBUM_NAME_LENGTH: Number(
                process.env.VITE_MAX_ALBUM_NAME_LENGTH
            ),
            CLIP_PAGE_COUNT: Number(process.env.VITE_CLIP_PAGE_COUNT),
            MAX_CLIP_NAME_LENGTH: Number(process.env.VITE_MAX_CLIP_NAME_LENGTH),
            MAX_YOUTUBE_VIDEOID_LENGTH: Number(
                process.env.VITE_MAX_YOUTUBE_VIDEOID_LENGTH
            ),
            MAX_GENRE_NAME_LENGTH: Number(
                process.env.VITE_MAX_GENRE_NAME_LENGTH
            ),
            MAX_SELECT_GENRES_COUNT: Number(
                process.env.VITE_MAX_SELECT_GENRES_COUNT
            ),
            MAX_TELEGRAM_USERNAME_LENGTH: Number(
                process.env.VITE_MAX_TELEGRAM_USERNAME_LENGTH
            ),
            MAX_YOUTUBE_CHANNEL_ID_LENGTH: Number(
                process.env.VITE_MAX_YOUTUBE_CHANNEL_ID_LENGTH
            ),
            MAX_VK_USERNAME_LENGTH: Number(
                process.env.VITE_MAX_VK_USERNAME_LENGTH
            ),
            DATE_FORMAT: process.env.VITE_DATE_FORMAT,
            ALBUM_PAGE_COUNT: Number(process.env.VITE_ALBUM_PAGE_COUNT),
            MAX_PLAYLIST_NAME_LENGTH: Number(
                process.env.VITE_MAX_PLAYLIST_NAME_LENGTH
            ),
            MAX_PLAYLIST_DESCRIPTION_LENGTH: Number(
                process.env.VITE_MAX_PLAYLIST_DESCRIPTION_LENGTH
            ),
            AUTOCOMPLETE_SEARCH_ALBUM_LIMIT: Number(
                process.env.VITE_AUTOCOMPLETE_SEARCH_ALBUM_LIMIT
            ),
            AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT: Number(
                process.env.VITE_AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT
            ),
            AUTOCOMPLETE_SEARCH_TRACK_LIMIT: Number(
                process.env.VITE_AUTOCOMPLETE_SEARCH_TRACK_LIMIT
            ),
            AUTOCOMPLETE_SEARCH_CLIP_LIMIT: Number(
                process.env.VITE_AUTOCOMPLETE_SEARCH_CLIP_LIMIT
            ),
            AUTOCOMPLETE_SEARCH_PLAYLIST_LIMIT: Number(
                process.env.VITE_AUTOCOMPLETE_SEARCH_PLAYLIST_LIMIT
            ),
            SEARCH_ALBUM_LIMIT: Number(process.env.VITE_SEARCH_ALBUM_LIMIT),
            SEARCH_MUSICIAN_LIMIT: Number(
                process.env.VITE_SEARCH_MUSICIAN_LIMIT
            ),
            SEARCH_CLIP_LIMIT: Number(process.env.VITE_SEARCH_CLIP_LIMIT),
            SEARCH_PLAYLIST_LIMIT: Number(
                process.env.VITE_SEARCH_PLAYLIST_LIMIT
            ),
            SEARCH_GENRE_LIMIT: Number(process.env.VITE_SEARCH_GENRE_LIMIT),
            MAX_IMAGE_FILE_SIZE_MB: Number(process.env.MAX_IMAGE_FILE_SIZE_MB),
            MAX_TRACK_FILE_SIZE_MB: Number(process.env.MAX_TRACK_FILE_SIZE_MB),
            MAX_SLIDE_FILE_SIZE_MB: Number(process.env.MAX_SLIDE_FILE_SIZE_MB),
            MAX_CHANGE_ROLE_FILES_SIZE_MB: Number(
                process.env.MAX_CHANGE_ROLE_FILES_SIZE_MB
            ),
            CHANGE_ROLE_PAGE_ITEMS: Number(process.env.CHANGE_ROLE_PAGE_ITEMS),
            SLIDER_PAGE_ITEMS: Number(process.env.SLIDER_PAGE_ITEMS),
            MAX_SLIDE_NAME_LENGTH: Number(process.env.MAX_SLIDE_NAME_LENGTH),
            SLIDER_ASPECT_RATIO: Number(process.env.SLIDER_ASPECT_RATIO),
            YOUTUBE_EMBED_URL: process.env.YOUTUBE_EMBED_URL,
            MUSICIAN_ALL_TRACKS_LIMIT: Number(
                process.env.MUSICIAN_ALL_TRACKS_LIMIT
            ),
            YOUTUBE_VIDEO: process.env.YOUTUBE_VIDEO,
            HISTORY_ALL_TRACKS_LIMIT: Number(
                process.env.HISTORY_ALL_TRACKS_LIMIT
            ),
            FAVORITE_ALBUMS_LIMIT: Number(process.env.FAVORITE_ALBUMS_LIMIT),
            LAST_ALBUMS_LIMIT: Number(process.env.LAST_ALBUMS_LIMIT),
            POPULAR_TRACKS_LIMIT: Number(process.env.POPULAR_TRACKS_LIMIT),
            GENRES_ALL_LIMIT: Number(process.env.GENRES_ALL_LIMIT),
            FAVORITE_MUSICIANS_LIMIT: Number(
                process.env.FAVORITE_MUSICIANS_LIMIT
            ),
            FAVORITE_TRACKS_LIMIT: Number(process.env.FAVORITE_TRACKS_LIMIT),
            POPULAR_TRACKS_LIMIT_ALL: Number(
                process.env.POPULAR_TRACKS_LIMIT_ALL
            ),
            POPULAR_ALBUMS_LIMIT: Number(process.env.POPULAR_ALBUMS_LIMIT),
            POPULAR_ALBUMS_LIMIT_ALL: Number(
                process.env.POPULAR_ALBUMS_LIMIT_ALL
            ),
            POPULAR_MUSICIANS_LIMIT: Number(
                process.env.POPULAR_MUSICIANS_LIMIT
            ),
            POPULAR_MUSICIANS_LIMIT_ALL: Number(
                process.env.POPULAR_MUSICIANS_LIMIT_ALL
            ),
            USER_PLAYLISTS_LIMIT: Number(process.env.USER_PLAYLISTS_LIMIT),
            MAX_EMAIL_LENGTH: Number(process.env.MAX_EMAIL_LENGTH),
            MAX_SUPPORT_MESSAGE_LENGTH: Number(
                process.env.MAX_SUPPORT_MESSAGE_LENGTH
            ),
            SUPPORT_MESSAGES_PAGE_SIZE: Number(
                process.env.SUPPORT_MESSAGES_PAGE_SIZE
            ),
        },
    },
});
