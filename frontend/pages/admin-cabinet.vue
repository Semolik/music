<template>
    <SettingsMenu :links="linksAll" indexRouteName="admin-cabinet">
        <NuxtPage />
    </SettingsMenu>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";

useHead({
    title: "Кабинет администратора",
});
definePageMeta({
    middleware: ["admin"],
});

const linksAll = [
    {
        text: "Список жанров",
        to: {
            name: routesNames.adminCabinet.cabinetGenres,
        },
        icon: IconsNames.listIcon,
    },
    {
        text: "Запросы стать музыкантом",
        to: {
            name: routesNames.adminCabinet.cabinetRequests,
        },
        icon: IconsNames.changeIcon,
    },
    {
        text: "Слайдер",
        to: {
            name: routesNames.adminCabinet.cabinetSlider,
        },
        icon: IconsNames.imageIcon,
    },
    {
        text: "Запросы в поддержку",
        to: {
            name: routesNames.adminCabinet.cabinetSupport,
        },
        icon: IconsNames.supportIcon,
    },
];
</script>
