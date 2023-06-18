<template>
    <div class="filters-panel">
        <slot></slot>
        <div
            v-for="(name, key) in items"
            :class="['filter', { active: active === key }, key]"
            @click="emit('update:active', key)"
        >
            {{ name }}
        </div>
    </div>
</template>
<script setup>
const { items, active } = defineProps({
    items: {
        type: Object,
        default: null,
    },
    active: {
        type: String,
        default: null,
    },
});
const emit = defineEmits(["update:active"]);
</script>
<style scoped lang="scss">
.filters-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    width: 100%;
    .filter {
        background-color: $quinary-bg;
        padding: 5px 20px;
        border-radius: 5px;
        cursor: pointer;
        color: $primary-text;
        user-select: none;
        flex-grow: 1;
        text-align: center;
        &.active {
            background-color: $accent;
            color: $primary-bg;
        }
    }
}
</style>
