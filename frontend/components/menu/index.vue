<template>
    <div class="menu">
        <div class="menu-title">Меню</div>
        <div class="menu-selection">
            <MenuCard
                v-if="!logined"
                :to="{ name: routesNames.login }"
                :icon="IconsNames.loginIcon"
                text="Войти"
            />
            <MenuCard
                :to="{ name: routesNames.settings.profile }"
                :icon="IconsNames.userIcon"
                text="Личный кабинет"
                v-else
            />
        </div>
        <div class="menu-selection" v-for="selection in menuSelections">
            <div class="menu-selection-title" v-if="selection.name">
                {{ selection.name }}
            </div>
            <div class="menu-selection-items">
                <MenuCard v-for="link in selection.links" v-bind="link" />
            </div>
        </div>
    </div>
</template>
<script setup>
import { menuSelections } from "@/configs/selections";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
const { logined } = storeToRefs(useAuthStore());
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
