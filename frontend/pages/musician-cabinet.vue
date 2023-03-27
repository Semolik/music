<template>
    <SettingsMenu :links="linksAll" indexRouteName="musician-cabinet">
        <NuxtPage />
    </SettingsMenu>
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
        text: "Профиль",
        to: {
            name: routesNames.musicianCabinet.cabinetProfile,
        },
        icon: IconsNames.userIcon,
    },
    {
        text: "Альбомы",
        to: {
            name: routesNames.musicianCabinet.cabinetAlbums,
        },
        icon: IconsNames.albumIcon,
    },
];
</script>
