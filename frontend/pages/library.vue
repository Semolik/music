<template>
    <NuxtPage />
</template>
<script setup>
import { routesNames } from "@typed-router";
import { useHeaderStore } from "~/stores/header";

const headerStore = useHeaderStore();

const route = useRoute();
definePageMeta({
    middleware: ["auth"],
});
const links = [
    {
        name: routesNames.library.playlists,
        title: "Плейлисты",
    },
    {
        name: routesNames.library.tracks,
        title: "Треки",
    },
    {
        name: routesNames.library.albums,
        title: "Альбомы",
    },
    {
        name: routesNames.library.artists,
        title: "Исполнители",
    },
    {
        name: routesNames.library.history,
        title: "История",
    },
];
const router = useRouter();

watch(
    router.currentRoute,
    async (value) => {
        headerStore.setTitle("Библиотека");
        headerStore.links = links;
        if (value.name === "library") {
            router.push({ name: "library-playlists" });
            return;
        }
        headerStore.currentRouteName = route.name;
    },
    { immediate: true }
);
</script>
