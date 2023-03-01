<template>
    <aside v-bind="$attrs">
        <div class="selections">
            <MenuItem :to="{ name: 'index' }" :icon="homeIcon" text="Главная" />
            <MenuItem
                :to="{ name: 'history' }"
                :icon="historyIcon"
                text="История прослушивания"
            />
            <MenuItem
                :to="{ name: 'favorite-tracks' }"
                :icon="trackIcon"
                text="Треки"
            />
            <MenuItem
                :to="{ name: 'favorite-albums' }"
                :icon="albumIcon"
                text="Альбомы"
            />
            <MenuItem
                :to="{ name: 'favorite-artists' }"
                :icon="musicianIcon"
                text="Исполнители"
            />
            <MenuItem
                :to="{ name: 'favorite-playlists' }"
                :icon="playlistIcon"
                text="Плейлисты"
            />
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
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
const runtimeConfig = useRuntimeConfig();

const {
    playlistIcon,
    albumIcon,
    trackIcon,
    musicianIcon,
    homeIcon,
    historyIcon,
    loginIcon,
} = runtimeConfig.public;
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

    .selections {
        display: flex;
        flex-direction: column;
        gap: 10px;
        flex-grow: 1;
    }
}
</style>
