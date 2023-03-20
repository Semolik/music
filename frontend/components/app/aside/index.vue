<template>
    <aside v-bind="$attrs">
        <div class="selections">
            <MenuItem :to="{ name: 'index' }" :icon="homeIcon" text="Главная" />
            <template v-for="selection in menuSelections">
                <div class="selection-title" v-if="selection.name">
                    {{ selection.name }}
                </div>
                <MenuItem v-for="link in selection.links" v-bind="link" />
            </template>
        </div>

        <div class="account-info">
            <MenuItem
                :to="{ name: 'login' }"
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
            <AppAsideProfile
                v-if="logined"
                :fullName="authStore.fullName"
                :picture="userData?.picture"
            />
            <MenuItem
                :to="{ name: 'login' }"
                :icon="loginIcon"
                text="Войти в аккаунт"
                v-else
            />
        </div>
    </aside>
</template>
<script setup>
import { menuSelections } from "~~/configs/selections";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { IconsNames } from "@/configs/icons";
const { homeIcon, loginIcon } = IconsNames;
const authStore = useAuthStore();
const { logined, userData, isMusician, isAdmin } = storeToRefs(authStore);
</script>
<style lang="scss">
aside {
    background-color: $secondary-bg;
    padding: 15px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    min-width: 300px;

    .selections {
        display: flex;
        flex-direction: column;
        gap: 10px;
        flex-grow: 1;

        .selection-title {
            margin-top: 20px;
            font-weight: bold;
            color: $secondary-text;
        }
    }
    .account-info {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
}
</style>
