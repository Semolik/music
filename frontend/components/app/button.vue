<template>
    <div :class="['app-button', { active: active }]">
        <slot />
    </div>
</template>
<script setup>
const { active } = defineProps({
    active: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss">
.app-button {
    @include flex-center;
    cursor: pointer;
    background-color: $quaternary-bg;
    padding: 10px;
    height: min-content;
    border-radius: 10px;
    width: 100%;
    cursor: default;
    user-select: none;

    &.active {
        background-color: $accent;
        color: black;
        cursor: pointer;

        &:hover {
            background-color: $accent-hover;
        }
    }
}
</style>
