<template>
    <ClientOnly v-if="animate">
        <div v-auto-animate :class="['tracks', { grid }]">
            <slot />
        </div>
    </ClientOnly>
    <div :class="['tracks', { grid }]" v-else>
        <slot />
    </div>
</template>
<script setup>
const { grid, cut, cutCount } = defineProps({
    grid: {
        type: Boolean,
        default: false,
    },
    cut: {
        type: Boolean,
        default: false,
    },
    animate: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.tracks {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    &.grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        grid-template-rows: min-content;
        height: min-content;
        @include lg(true) {
            grid-template-columns: 1fr;
        }

        & > * {
            flex-grow: 1;
        }

        & > :nth-last-child(n + 7) {
            display: none;
        }
    }
}
</style>
