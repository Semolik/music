// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: [
        "nuxt-icon",
        "@element-plus/nuxt",
        "@nuxtjs/tailwindcss",
        "@nuxtjs/google-fonts",
        "@pinia/nuxt",
    ],
    ssr: true,
    runtimeConfig: {
        public: {
            musicianIcon: "material-symbols:person-rounded",
            albumIcon: "material-symbols:album",
            trackIcon: "material-symbols:music-note-rounded",
            playlistIcon: "material-symbols:playlist-add",
        },
    },
    googleFonts: {
        families: {
            "Open+Sans": true,
        },
    },
    plugins: [{ src: "~/plugins/autoAnimatePlugin.js", mode: `client` }],
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
});
