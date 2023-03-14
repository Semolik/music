<template>
    <div class="settings-container">
        <div class="settings">
            <div
                class="settings-aside"
                v-if="$viewport.isGreaterOrEquals('lg')"
            >
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
                    :to="{
                        name: 'setup-genres',
                        query: {
                            onlyGenres: true,
                        },
                    }"
                >
                    <Icon :name="IconsNames.guitarIcon" />
                    <span>Жанры</span>
                </nuxt-link>
                <div class="settings-aside-item" @click="logout">
                    <Icon :name="IconsNames.logoutIcon" />
                    <span>Выйти</span>
                </div>
            </div>
            <nuxt-link
                class="back-button"
                :to="{
                    name: isIndex ? routesNames.mobileMenu : 'settings',
                }"
                v-if="$viewport.isLessThan('lg')"
            >
                <Icon name="material-symbols:arrow-back" />
                <span> Назад {{ isIndex ? "" : "к настройкам" }} </span>
            </nuxt-link>
            <Menu
                v-if="$viewport.isLessThan('lg') && isIndex"
                :menuSelections="[selection]"
                hideTitle
            />

            <div
                class="settings-content"
                v-if="$viewport.isGreaterOrEquals('lg') || !isIndex"
            >
                <div
                    class="open-selection-message"
                    v-if="$viewport.isGreaterOrEquals('lg') && isIndex"
                >
                    <span>Выберите раздел</span>
                </div>
                <NuxtPage />
            </div>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
import { useAuthStore } from "~~/stores/auth";
useHead({
    title: "Настройки",
});
definePageMeta({
    middleware: ["auth"],
});
const { logoutRequest } = useAuthStore();
const router = useRouter();
const logout = () => {
    logoutRequest();
    router.push("/");
};
const isIndex = computed(() => router.currentRoute.value.name === "settings");
const selection = {
    name: null,
    links: [
        {
            text: "Профиль",
            to: {
                name: "settings-profile",
            },
            icon: IconsNames.userIcon,
        },
        {
            text: "Безопасность",
            to: {
                name: "settings-security",
            },
            icon: IconsNames.securityIcon,
        },
        {
            text: "Жанры",
            to: {
                name: "setup-genres",
            },
            icon: IconsNames.guitarIcon,
        },
        {
            text: "Выйти",
            onClick: logout,
            icon: IconsNames.logoutIcon,
        },
    ],
};
</script>
<style lang="scss" scoped>
.settings-container {
    height: 100%;
    display: flex;
    justify-content: center;
    height: min-content;
    @include lg {
        padding-top: 10vh;
    }
    .settings {
        width: 100%;
        height: 100%;
        max-width: 1200px;
        display: grid;
        grid-template-columns: 300px 1fr;
        overflow: hidden;
        @include lg(true) {
            grid-template-columns: 1fr;
            gap: 10px;
        }
        @include lg {
            border-radius: 15px;
            background-color: $secondary-bg;
        }

        &-aside {
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            @include lg(true) {
                padding: 10px;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            }
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
        .back-button {
            display: flex;
            gap: 10px;
            align-items: center;
            text-decoration: none;
            color: $secondary-text;
            padding: 10px;
            border-radius: 10px;
            cursor: pointer;
            @include lg(true) {
                background-color: $tertiary-bg;
                padding: 10px;
                span {
                    text-align: center;
                    width: 100%;
                }
            }
            @include lg {
                &:hover {
                    background-color: $tertiary-bg;
                }
            }

            svg {
                width: 20px;
                height: 20px;
                fill: $secondary-text;
                @include lg(true) {
                    width: 30px;
                    height: 30px;
                }
            }
        }
        &-content {
            width: 100%;
            height: 100%;
            background-color: $tertiary-bg;
            display: flex;
            flex-direction: column;
            color: $primary-text;
            padding: 10px;
            @include lg(true) {
                border-radius: 10px;
            }
            .open-selection-message {
                @include flex-center;
                height: 100%;
                color: $secondary-text;
            }
        }
    }
}
</style>
