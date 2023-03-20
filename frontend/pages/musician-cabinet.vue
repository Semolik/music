<template>
    <SettingsMenu :links="linksAll" indexRouteName="musician-cabinet" />
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";

useHead({
    title: "Кабинет музыканта",
});
definePageMeta({
    middleware: ["musician"],
});

const linksAll = [
    {
        text: "Альбомы",
        to: {
            name: routesNames.adminCabinet.cabinetAlbums,
        },
        icon: IconsNames.albumIcon,
    },
];
</script>
