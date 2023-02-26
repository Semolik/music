// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
    modules: [
        "nuxt-icon",
        "@element-plus/nuxt",
        "@nuxtjs/tailwindcss",
        "@nuxtjs/google-fonts",
        "@pinia/nuxt",
        "@vueuse/nuxt",
    ],
    ssr: true,

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
            musicianIcon: "material-symbols:person-rounded",
            albumIcon: "material-symbols:album",
            trackIcon: "material-symbols:music-note-rounded",
            playlistIcon: "material-symbols:playlist-add",
            likeIcon: "material-symbols:favorite",
            playIcon: "material-symbols:play-arrow",
            dotsIcon: "material-symbols:more-horiz",

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
        },
    },
});
