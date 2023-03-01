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
const runtimeConfig = useRuntimeConfig();
const { homeIcon, menuIcon, searchIcon } = runtimeConfig.public;
</script>
<style lang="scss" scoped>
.bottom-bar {
    background-color: $secondary-bg;
    position: static;
    bottom: 100vh;
    padding-bottom: env(safe-area-inset-bottom);
    left: 0;
    width: 100%;
    display: flex;
    padding: 5px;
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
