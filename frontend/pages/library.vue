<template>
    <NuxtPage />
</template>
<script setup>
definePageMeta({
    middleware: ["auth"],
    headerLinks: [
        {
            name: "library-playlists",
            title: "Плейлисты",
        },
        {
            name: "library-tracks",
            title: "Треки",
        },
        {
            name: "library-albums",
            title: "Альбомы",
        },
        {
            name: "library-artists",
            title: "Исполнители",
        },
    ],
    title: "Библиотека",
});

const router = useRouter();

if (!router.currentRoute.value.name) {
    router.push({ name: "library-playlists" });
}
</script>
