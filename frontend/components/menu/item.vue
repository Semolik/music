<template>
    <NuxtLink
        :to="to"
        :class="[
            'menu-link',
            {
                active: active,
                center: !icon,
                highlight: highlight,
                'only-mini-icon': onlyMiniIcon,
            },
        ]"
    >
        <Icon :name="icon" v-if="icon" />
        <span>{{ text }}</span>
    </NuxtLink>
</template>
<script setup>
const { to, icon, text, active, highlight, onlyMiniIcon } = defineProps({
    to: {
        type: Object,
    },
    icon: {
        type: String,
    },
    text: {
        type: String,
        required: true,
    },
    active: {
        type: Boolean,
        default: false,
    },
    highlight: {
        type: Boolean,
        default: false,
    },
    onlyMiniIcon: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss">
.menu-link {
    @include flex-center;
    text-decoration: none;
    gap: 10px;
    padding: 13px;
    border-radius: 5px;
    color: $secondary-text;
    cursor: pointer;
    &.highlight,
    &.active {
        background-color: $tertiary-bg;
        @include xxl(true) {
            &.highlight {
                background-color: transparent;
            }
        }
    }
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
        &.highlight {
            background-color: $quaternary-bg;
        }
        @include xxl(true) {
            background-color: $quinary-bg;
        }
        background-color: $tertiary-bg;
    }
    svg {
        width: 25px;
        height: 25px;
        color: $primary-text;
        transition: color 0s;
    }
    &.center {
        span {
            text-align: center;
            width: 100%;
            @include flex-center;
            margin: 0;
        }
    }
    &.only-mini-icon {
        @include xxl {
            svg {
                display: none;
            }
        }
    }
    span {
        flex-grow: 1;
        display: flex;
        align-items: center;
        margin-right: 20px;
        white-space: nowrap;
        @include xxl(true) {
            display: none;
        }
    }
}
</style>
