<template>
    <div class="bottom-bar">
        <nuxt-link :to="{ name: 'index' }">
            <Icon :name="homeIcon" />
        </nuxt-link>
        <nuxt-link :to="{ name: 'mobile-search' }">
            <Icon :name="searchIcon" />
        </nuxt-link>
        <nuxt-link :to="{ name: 'mobile-menu' }">
            <Icon :name="menuIcon" />
        </nuxt-link>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { homeIcon, menuIcon, searchIcon } = IconsNames;
</script>
<style lang="scss" scoped>
.bottom-bar {
    border-top: 1px solid $tertiary-bg;
    background-color: $secondary-bg;
    position: fixed;
    bottom: 0;
    padding-bottom: env(safe-area-inset-bottom);
    left: 0;
    width: 100%;
    display: flex;
    padding: 5px;
    z-index: 1000;
    height: 70px;
    a {
        @include flex-center;
        flex-grow: 1;
        padding: 15px;
        text-decoration: none;
        color: $tertiary-text;
        border-radius: 5px;
        &.router-link-active {
            color: $primary-text;
            background-color: $tertiary-bg;
        }
        svg {
            width: 25px;
            height: 25px;
        }
    }
}
</style>
