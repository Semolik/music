<template>
    <NuxtPage />
</template>
<script setup>
definePageMeta({
    middleware: ["auth"],
    title: "Популярные треки",
    headerLinks: [
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
    ],
});
</script>
