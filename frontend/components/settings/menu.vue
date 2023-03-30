<template>
    <div class="settings-container">
        <div class="settings">
            <div
                class="settings-aside"
                v-if="$viewport.isGreaterOrEquals('lg')"
            >
                <template v-for="item in selection.links">
                    <nuxt-link
                        class="settings-aside-item"
                        :key="item.text"
                        :to="item.to"
                        v-if="item.to"
                    >
                        <Icon :name="item.icon" />
                        <span>{{ item.text }}</span>
                    </nuxt-link>
                    <div
                        class="settings-aside-item"
                        v-else
                        @click="item.onClick"
                    >
                        <Icon :name="item.icon" />
                        <span>{{ item.text }}</span>
                    </div>
                </template>
            </div>
            <nuxt-link
                class="back-button"
                :to="{
                    name: isIndex ? routesNames.mobileMenu : indexRouteName,
                }"
                v-if="$viewport.isLessThan('lg')"
            >
                <Icon :name="IconsNames.backIcon" />
                <span>Назад</span>
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
                <slot />
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { RoutePathByName, routesNames } from "@typed-router";
import { IconsNames } from "~~/configs/icons";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { UserTypeEnum } from "@/client/models/UserTypeEnum";
interface menuLink {
    text: string;
    to?: {
        name: string;
        query?: Record<string, string>;
    };
    icon: string;
    onClick?: () => void;
    UserType?: UserTypeEnum;
}
const { links, indexRouteName } = defineProps<{
    links: menuLink[];
    indexRouteName: RoutePathByName;
}>();
const { isMusician, isAdmin, isUser } = storeToRefs(useAuthStore());
const route = useRoute();
const isIndex = computed(() => route.name === indexRouteName);

const selection = computed(() => {
    return {
        name: null,
        links: links.filter(
            (link) =>
                (link.UserType === UserTypeEnum.SUPERUSER && isAdmin.value) ||
                (link.UserType === UserTypeEnum.USER && isUser.value) ||
                (link.UserType === UserTypeEnum.MUSICIAN && isMusician.value) ||
                !link.UserType
        ),
    };
});
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
            overflow: auto;
            max-height: 70vh;
            @include lg(true) {
                border-radius: 10px;
                height: min-content;
                max-height: 100%;
                height: 100%;
                overflow: visible;
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
