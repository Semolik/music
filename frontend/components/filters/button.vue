<template>
    <div :class="['filters-button', { active: active }]">
        <slot />
    </div>
</template>
<script setup>
defineProps({
    active: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.filters-button {
    @include flex-center;
    border-radius: 10px;
    padding: 5px 20px;
    gap: 5px;
    background-color: $tertiary-bg;
    cursor: pointer;
    color: $secondary-text;
    user-select: none;

    @include lg(true) {
        flex-grow: 1;
    }
    &.active {
        background-color: $accent;
        color: $primary-bg;

        &:hover {
            background-color: $accent-hover;
        }
    }

    &:not(.active):hover {
        background-color: $quaternary-bg;
    }
}
</style>
