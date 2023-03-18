<template>
    <div :class="['app-button', { active: active }]">
        <slot />
    </div>
</template>
<script setup>
const { active, borderRadius } = defineProps({
    active: {
        type: Boolean,
        default: false,
    },
    borderRadius: {
        type: String,
        default: "10px",
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
    border-radius: v-bind(borderRadius);
    width: 100%;
    cursor: default;
    user-select: none;

    &.active {
        background-color: var(--app-button-active-bg, $accent);
        color: black;
        cursor: pointer;

        &:hover {
            background-color: var(--app-button-active-hover-bg, $accent-hover);
        }
    }
}
</style>
