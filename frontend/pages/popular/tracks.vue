<template>
    <NuxtPage />
</template>
<script setup>
import { useHeaderStore } from "~/stores/header";
import { routesNames } from "@typed-router";
const headerStore = useHeaderStore();
const route = useRoute();
const { setTitle } = headerStore;
const links = [
    {
        name: routesNames.popularTracks.tracksWeek,
        title: "За неделю",
    },
    {
        name: routesNames.popularTracks.index,
        title: "За месяц",
    },
    {
        name: routesNames.popularTracks.tracksAll,
        title: "За все время",
    },
];
watch(
    () => route.name,
    async (value) => {
        if (!Object.values(routesNames.popularTracks).includes(value)) return;
        headerStore.reset();
        headerStore.currentRouteName = value;
        switch (value) {
            case "popular-tracks-week":
                setTitle("Популярные треки за неделю");
                break;
            case "popular-tracks":
                setTitle("Популярные треки за месяц");
                break;
            case "popular-tracks-all":
                setTitle("Популярные треки за все время");
                break;
        }
        headerStore.links = links;
    },
    { immediate: true }
);
</script>
