<template>
    <aside>
        <div class="selections">
            <NuxtLink to="/" class="selection">
                <Icon name="material-symbols:home-outline-rounded" />
                <span>Главная</span>
            </NuxtLink>
            <NuxtLink to="/history" class="selection">
                <Icon name="material-symbols:history-rounded" />
                <span>История прослушивания</span>
            </NuxtLink>
            <NuxtLink to="/favorite/tracks" class="selection">
                <Icon name="material-symbols:music-note-rounded" />
                <span>Треки</span>
            </NuxtLink>
            <NuxtLink to="/favorite/albums" class="selection">
                <Icon name="material-symbols:album" />
                <span>Альбомы</span>
            </NuxtLink>
            <NuxtLink to="/favorite/artists" class="selection">
                <Icon name="material-symbols:person-rounded" />
                <span>Исполнители</span>
            </NuxtLink>
            <NuxtLink to="/favorite/playlists" class="selection">
                <Icon name="material-symbols:playlist-play-rounded" />
                <span>Плейлисты</span>
            </NuxtLink>
        </div>
        <div class="account-info">
            <NuxtLink to="/profile" class="logined" v-if="logined">
                <span>{{ authStore.fullName }}</span>
            </NuxtLink>
            <NuxtLink to="/login" class="selection" v-else>
                <Icon name="material-symbols:login-rounded" />
                <span>Войти в аккаунт</span>
            </NuxtLink>
        </div>
    </aside>
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
</script>
<style lang="scss">
aside {
    background-color: $secondary-bg;
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    a.selection {
        @include flex-center;
        text-decoration: none;
        gap: 10px;
        padding: 13px;
        border-radius: 5px;
        color: $secondary-text;
        cursor: pointer;
        @include sm(true) {
            &:not(.mobile) {
                display: none;
            }
            &.menu {
                display: flex;
            }
        }

        &.router-link-active {
            @include sm {
                background-color: $tertiary-bg;
            }
            span,
            svg {
                color: $primary-text;
            }
            svg {
                &.default {
                    display: none;
                }
            }
        }
        &:not(.router-link-active) {
            span,
            svg {
                color: $secondary-text;
            }
            svg {
                &.active {
                    display: none;
                }
            }
        }
        @include sm {
            &:hover {
                background-color: $tertiary-bg;
            }
            &.menu {
                display: none;
            }
        }
        svg {
            width: 20px;
            height: 20px;
            color: $primary-text;
            transition: color 0s;
        }

        span {
            flex-grow: 1;
            display: flex;
            align-items: center;
            margin-right: 20px;
            white-space: nowrap;
        }
    }
    .selections {
        display: flex;
        flex-direction: column;
        gap: 10px;
        flex-grow: 1;
    }
    .account-info {
        display: flex;
        flex-direction: column;
        .logined {
            background-color: $tertiary-bg;
            text-decoration: none;
            gap: 10px;
            padding: 13px;
            border-radius: 5px;
            color: $secondary-text;
            cursor: pointer;
        }
    }
}
</style>
