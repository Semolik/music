<template>
    <NuxtPage />
</template>
<script setup>
import { useHeaderStore } from "~/stores/header";
const headerStore = useHeaderStore();
const route = useRoute();
const { setTitle } = headerStore;
const links = [
    {
        name: "popular-tracks-week",
        title: "За неделю",
    },
    {
        name: "popular-tracks",
        title: "За месяц",
    },
    {
        name: "popular-tracks-all",
        title: "За все время",
    },
];
watch(
    () => route.name,
    async (value) => {
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
