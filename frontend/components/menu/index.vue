<template>
    <div class="menu">
        <div class="menu-title" v-if="!hideTitle">{{ title }}</div>
        <div class="menu-selection" v-if="showLoginSelection">
            <MenuCard
                :to="{ name: routesNames.login }"
                :icon="IconsNames.loginIcon"
                text="Войти"
                v-if="!logined"
            />
            <template v-else>
                <MenuCard
                    :to="{ name: 'settings' }"
                    :icon="IconsNames.settingsIcon"
                    text="Настройки"
                />
                <MenuItem
                    :to="{ name: 'musician-cabinet' }"
                    text="Кабинет музыканта"
                    active
                    v-if="isMusician"
                />
                <MenuItem
                    :to="{ name: 'admin-cabinet' }"
                    text="Кабинет администратора"
                    active
                    v-if="isAdmin"
                />
                <MenuItem
                    :onClick="logoutRequest"
                    text="Выйти из аккаунта"
                    active
                />
            </template>
        </div>
        <div class="menu-selection" v-for="selection in menuSelections">
            <div class="menu-selection-title" v-if="selection.name">
                {{ selection.name }}
            </div>
            <div class="menu-selection-items">
                <MenuCard v-for="link in selection.links" v-bind="link" />
            </div>
        </div>
        <div class="menu-selection" v-if="logined"></div>
    </div>
</template>
<script setup>
import { menuSelections as menuSelectionsDefault } from "@/configs/selections";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
const authStore = useAuthStore();
const { logoutRequest } = authStore;
const { logined, isMusician, isAdmin } = storeToRefs(authStore);

const { menuSelections, title, hideTitle } = defineProps({
    menuSelections: {
        type: Array,
        default: menuSelectionsDefault,
    },
    showLoginSelection: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: "Меню",
    },
    hideTitle: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.menu {
    color: $secondary-text;
    display: flex;
    flex-direction: column;
    gap: 10px;

    .menu-title {
        margin-top: 20px;
        font-weight: bold;
        font-size: 25px;
        color: $secondary-text;
    }
    .menu-selection {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .menu-selection-title {
            margin-top: 20px;
            font-weight: bold;
            color: $secondary-text;
        }

        .menu-selection-items {
            display: grid;
            gap: 10px;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        }
    }
}
</style>
