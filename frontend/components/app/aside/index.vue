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
const { logined, userData } = storeToRefs(authStore);
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
}
</style>
