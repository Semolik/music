<template>
    <SettingsMenu :links="linksAll" indexRouteName="settings">
        <NuxtPage />
    </SettingsMenu>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
import { UserTypeEnum } from "@/client/models/UserTypeEnum";
useHead({
    title: "Настройки",
});
definePageMeta({
    middleware: ["auth"],
});

const linksAll = [
    {
        text: "Профиль",
        to: {
            name: routesNames.settings.profile,
        },
        icon: IconsNames.userIcon,
    },
    {
        text: "Безопасность",
        to: {
            name: routesNames.settings.security,
        },
        icon: IconsNames.securityIcon,
    },
    {
        text: "Жанры",
        to: {
            name: routesNames.setupGenres,
            query: {
                onlyGenres: true,
            },
        },
        icon: IconsNames.guitarIcon,
    },

    {
        text: "Стать музыкантом",
        to: {
            name: routesNames.settings.becomeMusician,
        },
        icon: IconsNames.changeIcon,
        UserType: UserTypeEnum.USER,
    },
];
</script>
