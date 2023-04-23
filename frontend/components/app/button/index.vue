<template>
    <div :class="['app-button', { active: active }, { 'no-accent': noAccent }]">
        <template v-if="!loading">
            <slot />
        </template>
        <div v-else class="loading">
            <Icon name="eos-icons:loading" />
        </div>
    </div>
</template>
<script setup>
const { active, borderRadius, loading } = defineProps({
    active: {
        type: Boolean,
        default: false,
    },
    borderRadius: {
        type: String,
        default: "10px",
    },
    noAccent: {
        type: Boolean,
        default: false,
    },
    loading: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss">
.app-button {
    @include flex-center;
    cursor: default;
    background-color: var(--app-button-bg, $quaternary-bg);
    padding: 10px;
    height: min-content;
    border-radius: v-bind(borderRadius);
    width: 100%;
    user-select: none;
    position: relative;
    overflow: hidden;

    &.active {
        background-color: var(--app-button-active-bg, $accent);

        color: black;
        cursor: pointer;
        &.no-accent {
            color: $primary-text;
            background-color: $quaternary-bg;
            &:hover {
                background-color: $quinary-bg;
            }
        }
        &:hover {
            background-color: var(--app-button-active-hover-bg, $accent-hover);
        }
    }
    .loading {
        @include flex-center;
        width: 100%;
        height: 100%;
        svg {
            width: 24px;
            height: 24px;
        }
    }
}
</style>
