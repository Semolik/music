<template>
    <div v-auto-animate class="cards-container">
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
});
const mdWidth = computed(() => props.mdWidth + "px");
const width = computed(() => props.width + "px");
</script>
