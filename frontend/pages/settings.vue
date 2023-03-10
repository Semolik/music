<template>
    <div class="settings-container">
        <div class="settings">
            <div class="settings-aside">
                <nuxt-link class="settings-aside-item" to="/settings/profile">
                    <Icon :name="IconsNames.userIcon" />
                    <span>Профиль</span>
                </nuxt-link>
                <nuxt-link class="settings-aside-item" to="/settings/security">
                    <Icon :name="IconsNames.securityIcon" />
                    <span>Безопасность</span>
                </nuxt-link>
                <nuxt-link
                    class="settings-aside-item"
                    :to="{ name: 'setup-genres', props: { nextPage: null } }"
                >
                    <Icon :name="IconsNames.guitarIcon" />
                    <span>Жанры</span>
                </nuxt-link>
                <div class="settings-aside-item" @click="logout">
                    <Icon :name="IconsNames.logoutIcon" />
                    <span>Выйти</span>
                </div>
            </div>
            <div class="settings-content">
                <NuxtPage />
            </div>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { useAuthStore } from "~~/stores/auth";
const { logoutRequest } = useAuthStore();
const router = useRouter();
const logout = () => {
    logoutRequest();
    router.push("/");
};
</script>
<style lang="scss" scoped>
.settings-container {
    height: 100%;
    display: flex;
    justify-content: center;
    padding-top: 10vh;
    height: min-content;
    .settings {
        background-color: $secondary-bg;
        width: 100%;
        height: 100%;
        max-width: 1200px;
        border-radius: 15px;
        display: grid;
        grid-template-columns: 300px 1fr;
        overflow: hidden;

        &-aside {
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            &-item {
                display: flex;
                gap: 10px;
                align-items: center;
                text-decoration: none;
                color: $secondary-text;
                padding: 8px;
                border-radius: 5px;
                cursor: pointer;

                &.router-link-active {
                    background-color: $tertiary-bg;
                    span,
                    svg {
                        color: $accent;
                    }
                    svg {
                        &.default {
                            display: none;
                        }
                    }
                }

                &:hover {
                    background-color: $tertiary-bg;
                }
                svg {
                    width: 20px;
                    height: 20px;
                    fill: $secondary-text;
                }
            }
        }
        &-content {
            width: 100%;
            height: 100%;
            background-color: $tertiary-bg;
        }
    }
}
</style>
