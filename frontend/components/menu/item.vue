<template>
    <NuxtLink :to="to" class="menu-link">
        <Icon :name="icon" />
        <span>{{ text }}</span>
    </NuxtLink>
</template>
<script setup>
const { to, icon, text } = defineProps({
    to: {
        type: Object,
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    text: {
        type: String,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.menu-link {
    @include flex-center;
    text-decoration: none;
    gap: 10px;
    padding: 13px;
    border-radius: 5px;
    color: $secondary-text;
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
    &:not(.router-link-active) {
        span,
        svg {
            color: $secondary-text;
        }
    }
    &:hover {
        background-color: $tertiary-bg;
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
</style>
