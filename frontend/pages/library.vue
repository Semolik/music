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
        {
            name: "library-history",
            title: "История",
        },
    ],
    title: "Библиотека",
});

const router = useRouter();

watch(
    router.currentRoute,
    (value) => {
        if (value.name === "library") {
            router.push({ name: "library-playlists" });
        }
    },
    { immediate: true }
);
</script>
