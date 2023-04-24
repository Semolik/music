<template>
    <aside v-bind="$attrs">
        <div class="selections">
            <MenuItem v-for="link in links" :key="link.text" v-bind="link" />
        </div>
        <div class="account-info">
            <template v-if="logined">
                <MenuItem
                    :to="{ name: 'settings' }"
                    text="Настройки"
                    highlight
                    :icon="IconsNames.settingsIcon"
                />
                <MenuItem
                    :to="{ name: 'musician-cabinet' }"
                    text="Кабинет музыканта"
                    :icon="IconsNames.userIcon"
                    highlight
                    v-if="isMusician"
                />
                <MenuItem
                    :to="{ name: 'admin-cabinet' }"
                    text="Кабинет администратора"
                    :icon="IconsNames.adminIcon"
                    highlight
                    v-if="isAdmin"
                />
                <MenuItem
                    @click="logout"
                    text="Выйти из аккаунта"
                    highlight
                    :icon="IconsNames.logoutIcon"
                />
            </template>
            <MenuItem
                :to="{ name: 'login' }"
                :icon="IconsNames.loginIcon"
                text="Войти в аккаунт"
                v-else
            />
        </div>
    </aside>
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { IconsNames } from "@/configs/icons";
import { useEventBus } from "@vueuse/core";
const links = [
    {
        to: { name: "index" },
        icon: IconsNames.homeIcon,
        text: "Главная",
    },
    {
        icon: IconsNames.searchIcon,
        text: "Поиск",
        onClick: () => {
            openSearchBus.emit();
        },
    },
    {
        to: { name: "library" },
        icon: IconsNames.libraryIcon,
        text: "Библиотека",
    },
];
const authStore = useAuthStore();
const { logoutRequest } = authStore;
const router = useRouter();
const logout = () => {
    router.push({ name: "index" });
    logoutRequest();
};
const openSearchBus = useEventBus("openSearch");
const { logined, isMusician, isAdmin } = storeToRefs(authStore);
</script>
<style lang="scss">
aside {
    background-color: $secondary-bg;
    padding: 15px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    min-width: 300px;
    @include xxl(true) {
        min-width: auto;
    }
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
