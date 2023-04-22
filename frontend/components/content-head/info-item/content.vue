<template>
    <div class="label" v-if="item.name">
        {{ item.name }}
    </div>
    <div :class="['value', { highlight: highlight }]">{{ item.value }}</div>
</template>
<script setup>
const { item } = defineProps({
    item: {
        type: Object,
        required: true,
    },
});

const highlight = computed(() => !!item.link);
</script>
<style lang="scss" scoped>
.value {
    color: $primary-text;

    &.highlight:hover {
        color: $accent;
    }
}
.label {
    color: $secondary-text;
}
</style>
