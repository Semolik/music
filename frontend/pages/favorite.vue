<template>
    <NuxtPage />
</template>
<script setup>
definePageMeta({
    middleware: ["auth"],
    headerLinks: [
        {
            name: "favorite-playlists",
            title: "Плейлисты",
        },
        {
            name: "favorite-tracks",
            title: "Треки",
        },
        {
            name: "favorite-albums",
            title: "Альбомы",
        },
        {
            name: "favorite-artists",
            title: "Исполнители",
        },
    ],
    title: "Библиотека",
});

const router = useRouter();

if (!router.currentRoute.value.name) {
    router.push({ name: "favorite-playlists" });
}
</script>
<style lang="scss" scoped>
.favorite-page-container {
    display: flex;
    flex-direction: column;
    .favorite-page-title {
        font-size: 2.5rem;
        font-weight: 500;
        color: $secondary-text;
    }
}
</style>
