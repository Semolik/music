<template>
    <ClientOnly v-if="animate">
        <div
            v-auto-animate
            :class="['cards-container', { 'one-line': props.oneLine }]"
        >
            <slot />
        </div>
    </ClientOnly>
    <div :class="['cards-container', { 'one-line': props.oneLine }]" v-else>
        <slot />
    </div>
</template>
<style lang="scss" scoped>
.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(v-bind(width), 1fr));
    gap: 10px;
    @include lg(true) {
        grid-template-columns: repeat(auto-fill, minmax(v-bind(mdWidth), 1fr));
    }
    grid-template-rows: min-content;
    height: min-content;
    &.one-line {
        grid-template-rows: 1fr;
        grid-auto-rows: 0;
        row-gap: 0px;
        column-gap: 10px;
        overflow-y: hidden;
    }
}
</style>
<script setup>
const props = defineProps({
    mdWidth: {
        type: Number,
        required: false,
        default: 150,
    },
    width: {
        type: Number,
        required: false,
        default: 170,
    },
    oneLine: {
        type: Boolean,
        required: false,
        default: false,
    },
    animate: {
        type: Boolean,
        required: false,
        default: false,
    },
});
const mdWidth = computed(() => props.mdWidth + "px");
const width = computed(() => props.width + "px");
</script>
